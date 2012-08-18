// Generated by CoffeeScript 1.3.3
(function() {

  $(document).ready(function() {
    var generate_preview, getData, images;
    images = {};
    $('.layout-tile').click(function() {
      $('.layout-tile.active').removeClass('active');
      $(this).addClass('active');
      return generate_preview();
    });
    $('.background-swatch').click(function() {
      $('.background-swatch').removeClass('active');
      $(this).addClass('active');
      return generate_preview();
    });
    $('.banner-place').click(function() {
      if ($('#banner-hide').is(':checked')) {
        return null;
      }
      $('.banner-place').removeClass('active');
      $(this).addClass('active');
      return generate_preview();
    });
    $("#banner-hide").on('change', function() {
      if ($("#banner-hide").is(':checked')) {
        $(".banner-place").addClass('disabled');
      } else {
        $(".banner-place").removeClass('disabled');
        $(".banner-place").removeClass('active');
      }
      return generate_preview();
    });
    generate_preview = function() {
      var payload;
      payload = getData();
      return $.post('/image/generate', payload, function(resp) {
        var img;
        img = document.createElement('img');
        img.src = resp.preview;
        $('.preview').empty();
        return $('.preview').append(img);
      });
    };
    getData = function() {
      var avatar_src, banner_placement, banner_src, bg_color, i, image_list, imgs, layout, max_length, payload, _i, _len;
      layout = $(".layout-tile.active").data('dimensions');
      layout = {
        x: layout,
        y: layout
      };
      bg_color = $(".background-swatch.active").data('color');
      avatar_src = images.avatar;
      banner_src = images.banner;
      banner_placement = $(".banner-place.active").data('banner');
      imgs = images.images;
      image_list = [];
      max_length = layout.x * layout.y > imgs.length ? imgs.length : layout.x * layout.y;
      for (_i = 0, _len = imgs.length; _i < _len; _i++) {
        i = imgs[_i];
        image_list.push(i);
      }
      payload = {
        layout_x: layout['x'],
        layout_y: layout['y'],
        background: bg_color,
        avatar: avatar_src,
        banner: JSON.stringify({
          src: banner_src,
          placement: banner_placement,
          showBanner: !$("#banner-hide").is(':checked')
        }),
        images: JSON.stringify(image_list)
      };
      return payload;
    };
    return (function() {
      return $.ajax({
        url: 'etsy/images',
        success: function(resp) {
          images = resp;
          return generate_preview();
        }
      });
    })();
  });

}).call(this);
