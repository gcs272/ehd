(($)->
    $.fn.flip = (options) ->
        settings = $.extend 
            "duration": "1s",
            options

        this.each ->
            # get front
            $front = $(this).find ".front"

            # get back
            $back = $(this).find ".back"

            # add styles to parent div
            $(this).css
                "-webkit-perspective": "800px",
                "-webkit-transform-style": "preserve-3d",
                "-webkit-transition": settings.duration

            # add styles to the front, back elements
            $(".front, .back", this).css
                display: 'block',
                "-webkit-backface-visibility": 'hidden',
                position: 'absolute'


            # rotate back initially to hide
            $back.css
                '-webkit-transform': "rotateY(180deg)"

            # set initial state
            $(this).data('rotated', false)

            # bind click events
            $(this).on 'click', (e) ->
                e.preventDefault()

                rotation = if $(this).data('rotated') == true then "rotateY(0deg)" else "rotateY(180deg)"

                $(this).css
                    '-webkit-transform': rotation

                $(this).data('rotated', !$(this).data('rotated'))


)(jQuery)