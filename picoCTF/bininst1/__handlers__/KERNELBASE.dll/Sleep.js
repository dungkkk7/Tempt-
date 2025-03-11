/*
 * Auto-generated by Frida. Please modify to match the signature of Sleep.
 * This stub is currently auto-generated from manpages when available.
 *
 * For full API reference, see: https://frida.re/docs/javascript-api/
 */

/*
 * Auto-generated by Frida. Please modify to match the signature of Sleep.
 * For full API reference, see: https://frida.re/docs/javascript-api/
 */

defineHandler({
  onEnter: function (log, args, state) {
    var sleepTime = args[0].toInt32(); // Đọc thời gian ngủ (DWORD, đơn vị ms)
    log("Sleep called with: " + sleepTime + " ms");
    args[0] = ptr(0); // Ghi đè thời gian ngủ thành 0ms
    log("Sleep time overridden to 0ms");
  }
});