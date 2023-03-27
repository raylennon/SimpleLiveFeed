$( document ).ready(function() {

    // Device
    var address = "10.194.145.32";
    var device = new Device(address);

    // Buttons

    document.addEventListener('keydown', (e) => {
      if (e.repeat) return;
      switch(e.keyCode) {
        case 38:
          device.callFunction("forward"); 
          console.log("Running forward!");
          break;
        case 37:
          device.callFunction("left");
          break;
        case 39:
          device.callFunction("right");
          break;
        case 40:
          device.callFunction("backward");
          break;
      } 
      console.log(e.key);
    });

    // $(document).keydown(function(e) {
    //   switch(e.which) {
    //     // case 38:
    //     //   device.callFunction("forward"); 
    //     //   break;
    //     case 37:
    //       device.callFunction("left");
    //       break;
    //     case 39:
    //       device.callFunction("right");
    //       break;
    //     case 40:
    //       device.callFunction("backward");
    //       break;
    //   } 
    // });
    $(document).keyup(function(e) {
      device.callFunction("stop");
    });
    $('#forward').mousedown(function() {
      device.callFunction("forward");
    });
    $('#forward').mouseup(function() {
      device.callFunction("stop");
    });

    $('#right').mousedown(function() {
      device.callFunction("right");
    });
    $('#right').mouseup(function() {
      device.callFunction("stop");
    });

    $('#left').mousedown(function() {
      device.callFunction("left");
    });
    $('#left').mouseup(function() {
      device.callFunction("stop");
    });

    $('#backward').mousedown(function() {
      device.callFunction("backward");
    });
    $('#backward').mouseup(function() {
      device.callFunction("stop");
    });

});
