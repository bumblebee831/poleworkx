/*global jQuery, flowplayer, window */
(function($) {

$(function() {    
    
    $(".myPlayListFlowPlayerAudio").each(function(index, value) {
        var config = jQuery.extend(true, {}, window.collective_flowplayer.config);
        var $self = $(this);
        var audio = $self.is('.audio');
        if (audio) { config.plugins.controls.fullscreen = false; }
        if ($self.is('.minimal')) { config.plugins.controls = null; }
        $self.append("<div id='myPlayListFlowPlayerAudio"+index+"'></div>");
        flowplayer("myPlayListFlowPlayerAudio"+index,window.collective_flowplayer.params, config).playlist(".myPlayListFlowPlayerAudio li", {loop: true, manual: true}).onLoad(initialVolume).onBeforeFinish(loop);
        
    })
});
}(jQuery));