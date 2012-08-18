$(document).ready ->
	images = {}

	$('.layout-tile').click ->
		$('.layout-tile.active').removeClass 'active'
		$(this).addClass 'active'
		generate_preview()

	$('.background-swatch').click ->
		$('.background-swatch').removeClass 'active'
		$(this).addClass 'active'
		generate_preview()

	$('.banner-place').click ->
		return null if $('#banner-hide').is ':checked'
		$('.banner-place').removeClass 'active'
		$(this).addClass 'active'
		generate_preview();

	$("#banner-hide").on 'change', ->
		if $("#banner-hide").is ':checked'
			$(".banner-place").addClass 'disabled'
		else
			$(".banner-place").removeClass 'disabled'
			$(".banner-place").removeClass 'active'

		generate_preview()

	generate_preview = ->
		payload = getData()
		$.post '/image/generate', payload, (resp) ->
			img = document.createElement 'img'
			img.src = resp.preview

			$('.preview').empty()
			$('.preview').append img

	getData = ->
		layout = $(".layout-tile.active").data 'dimensions'
		layout = 
			x: layout,
			y: layout
		
		bg_color = $(".background-swatch.active").data 'color'

		avatar_src = images.avatar
		banner_src = images.banner
		banner_placement = $(".banner-place.active").data 'banner'
		imgs = images.images
		image_list = []

		max_length = if (layout.x * layout.y > imgs.length) then imgs.length else layout.x * layout.y;

		image_list.push i for i in imgs

		payload =
			layout_x: layout['x'],
			layout_y: layout['y'],
			background: bg_color,
			avatar: avatar_src,
			banner: JSON.stringify
				src: banner_src,
				placement: banner_placement,
				showBanner: !$("#banner-hide").is ':checked'
			images: JSON.stringify image_list

		return payload

	(-> $.ajax
		url: 'etsy/images',
		success: (resp) ->
			images = resp
			generate_preview()
	)()