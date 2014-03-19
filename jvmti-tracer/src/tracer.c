#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <jvmti.h>

static FILE* out;

/**
 * Every JVMTI interface returns an error code, which should be checked to avoid
 * any cascading errors down the line. The function GetErrorName() returns the
 * actual enumeration constant name, making the error messages much easier to
 * understand.
 */
static void check_jvmti_error(jvmtiEnv *jvmti, jvmtiError error, const char *msg) {
    if (error != JVMTI_ERROR_NONE) {
        char *name = NULL;
        (*jvmti)->GetErrorName(jvmti, error, &name);
        fprintf(stderr, "ERROR: JVMTI: %d(%s): %s\n", error, (name == NULL ? "Unknown" : name), (msg == NULL ? "" : msg));
    }
}

/**
 * Only a single MethodEntry callback may be active at any one time.
 */
static jrawMonitorID callback_lock;

static void enter_critical_section(jvmtiEnv *jvmti, jrawMonitorID lock) {
    jvmtiError error = (*jvmti)->RawMonitorEnter(jvmti, lock);
    check_jvmti_error(jvmti, error, "Cannot enter with raw monitor");
}

static void exit_critical_section(jvmtiEnv *jvmti, jrawMonitorID lock) {
    jvmtiError error = (*jvmti)->RawMonitorExit(jvmti, lock);
    check_jvmti_error(jvmti, error, "Cannot exit with raw monitor");
}

static const int CALL_CHAIN_LENGTH = 2;

void JNICALL method_entry_callback(jvmtiEnv *jvmti, JNIEnv* jni, jthread thread, jmethodID mid) {
    jvmtiError error;
    int depth;
    jclass declaring_class; /* Unmanaged JNI object reference! */

    enter_critical_section(jvmti, callback_lock);

    fputs("CALL\t", out);

    for (depth = 0; depth < CALL_CHAIN_LENGTH; depth++) {
        char *method_name, *method_signature, *class_signature;
        char **const SKIP_GENERIC = NULL;

        jmethodID method;
        jlocation location;

        if ((error = (*jvmti)->GetFrameLocation(jvmti, thread, depth, &method, &location)) == JVMTI_ERROR_NO_MORE_FRAMES) {
            fputs("ROOT\n", out);
            break;
        }
        check_jvmti_error(jvmti, error, "ERROR\tCouldn't get frame location\n");

        error = (*jvmti)->GetMethodName(jvmti, method, &method_name, &method_signature, SKIP_GENERIC);
        check_jvmti_error(jvmti, error, "ERROR\tCouldn't get method name\n");

        error = (*jvmti)->GetMethodDeclaringClass(jvmti, method, &declaring_class);
        check_jvmti_error(jvmti, error, "ERROR\tCouldn't get declaring class\n");

        error = (*jvmti)->GetClassSignature(jvmti, declaring_class, &class_signature, SKIP_GENERIC);
        check_jvmti_error(jvmti, error, "ERROR\tCouldn't get class signature\n");

        (*jni)->DeleteLocalRef(jni, declaring_class);

        fputs(class_signature, out);
        fputc('\t', out);
        fputs(method_name, out);
        fputc('\t', out);
        fputs(method_signature, out);

        if (depth != CALL_CHAIN_LENGTH - 1)
            fputc('\t', out);
        else
            fputc('\n', out);

        error = (*jvmti)->Deallocate(jvmti, (unsigned char*) method_name);
        check_jvmti_error(jvmti, error, "ERROR\tCouldn't deallocate memory\n");
        error = (*jvmti)->Deallocate(jvmti, (unsigned char*) method_signature);
        check_jvmti_error(jvmti, error, "ERROR\tCouldn't deallocate memory\n");
        error = (*jvmti)->Deallocate(jvmti, (unsigned char*) class_signature);
        check_jvmti_error(jvmti, error, "ERROR\tCouldn't deallocate memory\n");
    }

    exit_critical_section(jvmti, callback_lock);
}

void JNICALL vm_death_callback(jvmtiEnv *jvmti, JNIEnv* jni) {
    /* All MethodEntry callbacks should be finished by now; otherwise, we get a JVMTI_ERROR_WRONG_PHASE. */
    /* Wait 1000 milliseconds to give them plenty time to finish */
    jvmtiError err = (*jvmti)->RawMonitorWait(jvmti, callback_lock, 1000);
}

static const jvmtiEventCallbacks callbacks = {
    .MethodEntry = &method_entry_callback,
    .VMDeath = &vm_death_callback
};

JNIEXPORT jint JNICALL Agent_OnLoad(JavaVM *jvm, char *options, void *reserved) {
    jvmtiEnv *jvmti = NULL;
    jvmtiCapabilities capabilities;
    jvmtiError error;

    /* Switch stdout with new file descriptor that writes to terminal */

    int stdout_copy = dup(1);
    int ttyfd = open("/dev/tty", O_RDWR);

    if (dup2(ttyfd, 1) == -1)
        return JNI_ERR;

    if (dup2(stdout_copy, ttyfd) == -1)
        return JNI_ERR;

    /* Make stream from file descriptor, to take advantage of buffering */

    out = fdopen(ttyfd, "w");

    if (out == NULL) {
        fprintf(stderr, "Couldn't make stream from file descriptor %d", ttyfd);
        return JNI_ERR;
    }

    if ((*jvm)->GetEnv(jvm, (void **) &jvmti, JVMTI_VERSION) != JNI_OK) {
        fprintf(stderr, "Couldn't get JVMTI environment");
        return JNI_ERR;
    }

    error = (*jvmti)->CreateRawMonitor(jvmti, "Tracer callbacks", &callback_lock);
    check_jvmti_error(jvmti, error, "Cannot create raw monitor");

    error = (*jvmti)->GetCapabilities(jvmti, &capabilities);
    check_jvmti_error(jvmti, error, "Couldn't get capabilities");

    capabilities.can_generate_method_entry_events = 1;

    error = (*jvmti)->AddCapabilities(jvmti, &capabilities);
    check_jvmti_error(jvmti, error, "Couldn't add capabilities");

    error = (*jvmti)->SetEventCallbacks(jvmti, &callbacks, sizeof(callbacks));
    check_jvmti_error(jvmti, error, "Couldn't set event callbacks");

    error = (*jvmti)->SetEventNotificationMode(jvmti, JVMTI_ENABLE, JVMTI_EVENT_METHOD_ENTRY, NULL);
    check_jvmti_error(jvmti, error, "Couldn't enable notification on method entry");

    error = (*jvmti)->SetEventNotificationMode(jvmti, JVMTI_ENABLE, JVMTI_EVENT_VM_DEATH, NULL);
    check_jvmti_error(jvmti, error, "Couldn't enable notification on VM death");

    return JNI_OK;
}

JNIEXPORT void JNICALL Agent_OnUnload(JavaVM *vm) {
    /* Can't hurt. */
    fflush(out);
    fclose(out);
}
