
defineHandler({
  onEnter: function (log, args, state) {
    log('WriteFile called:');
    log('  hFile: ' + args[0]);
    log('  lpBuffer pointer: ' + args[1]);
    var size = args[2].toInt32();
    log('  nNumberOfBytesToWrite: ' + size);
    if (size > 0) {
      log('  Data: ' + Memory.readUtf8String(args[1], size));
    } else {
      log('  No data to write (size = 0)');
      // Đọc 64 byte để lấy flag đầy đủ
      try {
        var bufferCheck = Memory.readByteArray(args[1], 64);
        log('  Buffer content (64 bytes): ' + hexdump(bufferCheck));
        var fullString = Memory.readUtf8String(args[1]);
        log('  Full string: ' + fullString);
      } catch (e) {
        log('  Buffer content: [Failed to read]');
      }
    }
  },
  onLeave: function (log, retval, state) {
    log('WriteFile returned: ' + retval);
  }
});
