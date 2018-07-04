/*
 * My speakers are connected to TV via optical TOSLINK and they are not
 * smart enough to be commanded by TV to change volume. My goal is to control
 * speaker volume with TV remote. This script accomplishes this goal by
 * subscribing to TV volume change and sends IR signal to change speaker volume.
 *
 * One problem is my TV disables volume change when audio output mode is optical.
 * As a workaround, I set audio mode to "Internal TV Speaker + Audio Out (Optical)".
 * To keep internal speaker silent, the volume is maintained at 0. In the event of
 * volume up key being pressed, the script sees volume changed to above 0, and it
 * sends IR signal and resets volume back to 0. Since the volume reset triggers
 * a volume change event, we use expectingVolumeDown to distinguish this kind
 * of volume change from user triggered ones. In the event of volume down key
 * being pressed, the script gets a volume change event, but volume is still 0,
 * indicating it's a volume down event.
 */
var lgtv = require("lgtv2")({
    url: 'ws://192.168.0.107:3000'
});
 
lgtv.on('connect', function () {
    console.log('connected');
    var exec = require('child_process').exec;
    var expectingVolumeDown = false;
    lgtv.subscribe('ssap://audio/getVolume', function (err, res) {
        if (res.action != "changed") {
            return;
        }
        if (res.volume > 0) {
            lgtv.request('ssap://audio/setVolume', {volume: 0});
            exec("irsend SEND_ONCE Edifier KEY_VOLUMEUP");
            expectingVolumeDown = true;
        } else if (!expectingVolumeDown) {
            exec("irsend SEND_ONCE Edifier KEY_VOLUMEDOWN");
        } else {
            expectingVolumeDown = false;
        }
    });
    
});
