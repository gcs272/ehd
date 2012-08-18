// Generated by CoffeeScript 1.3.3
(function() {

  (function($) {
    return $.fn.flip = function(options) {
      var settings;
      settings = $.extend({
        "duration": "1s"
      }, options);
      return this.each(function() {
        var $back, $front;
        $front = $(this).find(".front");
        $back = $(this).find(".back");
        $(this).css({
          "-webkit-perspective": "800px",
          "-webkit-transform-style": "preserve-3d",
          "-webkit-transition": settings.duration
        });
        $(".front, .back", this).css({
          display: 'block',
          "-webkit-backface-visibility": 'hidden',
          position: 'absolute'
        });
        $back.css({
          '-webkit-transform': "rotateY(180deg)"
        });
        $(this).data('rotated', false);
        return $(this).on('click', function(e) {
          var rotation;
          e.preventDefault();
          rotation = $(this).data('rotated') === true ? "rotateY(0deg)" : "rotateY(180deg)";
          $(this).css({
            '-webkit-transform': rotation
          });
          return $(this).data('rotated', !$(this).data('rotated'));
        });
      });
    };
  })(jQuery);

}).call(this);