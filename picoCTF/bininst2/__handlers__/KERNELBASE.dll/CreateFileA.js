/*
 * Auto-generated by Frida. Please modify to match the signature of CreateFileA.
 * This stub is currently auto-generated from manpages when available.
 *
 * For full API reference, see: https://frida.re/docs/javascript-api/
 */

defineHandler(
  {
    onEnter: function (log, args, state) {
      log('CreateFileA called:');
      log('  lpFileName: ' + Memory.readUtf8String(args[0]));
    },
    onLeave: function (log, retval, state) {
      log('CreateFileA returned: ' + retval);
      // Ghi đè giá trị trả về thành handle giả (ví dụ: 0x1234)
      retval.replace(0x1234);
      log('  Forced return value: 0x1234');
    }
  }
);
