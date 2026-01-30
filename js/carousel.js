(function ($) {

	const wdtCarouselWidgetHandler = function($scope, $) {

        setTimeout( function() {

            const $carouselItem = $scope.find('.wdt-carousel-holder');
            const $moduleId = $carouselItem.data('id');
            const $swiperItem = $carouselItem.find('.swiper');
            const $swiperUniqueId = $swiperItem.attr('id');
            const $swiperWrapper = $carouselItem.find('.swiper-wrapper');
            const $carouselSettings = $swiperItem.data('settings');

            if($carouselSettings === undefined) {
                return;
            }

            const $direction		  	= ($carouselSettings['direction'] !== undefined) ? ($carouselSettings['direction']) : 'horizontal';
            const $effect		  	    = ($carouselSettings['effect'] !== undefined) ? ($carouselSettings['effect']) : 'default';
            // const $grab_cursor          = ($effect == 'flip' || $effect == 'cards' || $effect == 'creative') ? true : false;
            const $free_mode            = ($effect == 'free_mode') ? true : false;
            const $slides_to_show	 	= ($carouselSettings['slides_to_show'] !== undefined) ? parseInt($carouselSettings['slides_to_show']) : 1;
            const $slides_to_scroll 	= ($carouselSettings['slides_to_scroll'] !== undefined) ? parseInt($carouselSettings['slides_to_scroll']) : 1;
            const $pagination			= ($carouselSettings['pagination'] !== undefined) ? ($carouselSettings['pagination']) : '';
            const $arrows			  	= ($carouselSettings['arrows'] !== undefined) ? ($carouselSettings['arrows'] == 'yes') : false;
            const $speed			 	= ($carouselSettings['speed'] !== undefined && $carouselSettings['speed'] != '') ? parseInt($carouselSettings['speed']) : 400;
            const $autoplay			  	= ($carouselSettings['autoplay'] !== undefined) ? ($carouselSettings['autoplay'] == 'yes') : false;
            const $autoplay_speed	 	= ($carouselSettings['autoplay_speed'] !== undefined && $carouselSettings['autoplay_speed'] != '') ? parseInt($carouselSettings['autoplay_speed']) : 20000;
            const $autoplay_direction   = ($carouselSettings['autoplay_direction'] !== undefined) ? ($carouselSettings['autoplay_direction']) : '';  
            const $allow_touch		    = ($carouselSettings['allow_touch'] !== undefined) ? ($carouselSettings['allow_touch'] == 'yes') : true;  
            const $loop				  	= ($carouselSettings['loop'] !== undefined) ? ($carouselSettings['loop'] == 'yes') : false;
            const $centered_slides		= ($carouselSettings['centered_slides'] !== undefined) ? ($carouselSettings['centered_slides'] == 'yes') : false;
            const $pause_on_interaction = ($carouselSettings['pause_on_interaction'] !== undefined) ? ($carouselSettings['pause_on_interaction'] == 'yes') : false;
            const $overflow_type		= ($carouselSettings['overflow_type'] !== undefined) ? ($carouselSettings['overflow_type']) : '';
            const $overflow_opacity = ($carouselSettings['overflow_opacity'] !== undefined) ? ($carouselSettings['overflow_opacity'] == 'yes') : false;
            const $unequal_height_compatability = ($carouselSettings['unequal_height_compatability'] === 'yes') ? true : false;
            const $space_between_gaps = $carouselSettings['space_between_gaps'];
            var $deviceMode = elementorFrontend.getCurrentDeviceMode();
            if( $deviceMode = 'widescreen' ) {
                $deviceMode = 'desktop';
            }
            const $space_between = $space_between_gaps[$deviceMode] ? $space_between_gaps[$deviceMode] : 0;
            const $mouse_wheel_scroll = ($carouselSettings['mouse_wheel_scroll'] === 'yes') ? true : false;

            // Initialize height if its vertical carousel
            if($direction == 'vertical') {
                const $height = parseInt($swiperItem.find('.swiper-slide:first .wdt-content-item').height(), 10) + 20;
                $swiperWrapper.css({'height':$height+'px'});
            }

            // Overflow script
            if($overflow_type == 'left') {

                const $itemOffsetLeft = $carouselItem.offset().left;
                const $itemPadding = parseInt($carouselItem.parents('.elementor-widget-wrap').css("padding-left"));
                const $itemLeft = (parseFloat($itemOffsetLeft) - parseFloat($itemPadding));
                const $itemWidth = $carouselItem.width();
                const $itemTotalWidth = parseFloat($itemWidth) + parseFloat($itemLeft);

                $swiperItem.css('width', $itemTotalWidth);
                $swiperItem.css('left', -$itemLeft);

            } else if($overflow_type == 'right') {

                const $docWidth = $(document).width();
                const $itemOffsetLeft = $carouselItem.offset().left;
                const itemOuterWidth = $carouselItem.outerWidth();
                const $itemWidth = $carouselItem.width();
                const itemRight = parseFloat($docWidth) - (parseFloat($itemOffsetLeft) + parseFloat(itemOuterWidth));
                const $itemPadding = parseInt($carouselItem.parents('.elementor-widget-wrap').css("padding-right"));
                const $itemTotalWidth = parseFloat($itemWidth) + parseFloat(itemRight) - parseFloat($itemPadding);

                $swiperItem.css('width', $itemTotalWidth);

            }
            const not_active_slide_scale_value = 0.85;
            const not_active_slide_opacity_value = 0.4;
            // Build swiper options
            const swiperOptions = {
                initialSlide: 0,
                simulateTouch: true,
                // roundLengths: true,
                keyboardControl: true,
                paginationClickable: true,
                autoHeight: false,
                // grabCursor: $grab_cursor,

                freeMode: $free_mode,
                allowTouchMove: $allow_touch,

                effect: $effect,
                fadeEffect: {
                    crossFade: true
                },
                coverflowEffect: {
                    rotate: 30,
                    slideShadows: false,
                },
                cubeEffect: {
                    slideShadows: false,
                },
                creativeEffect: {
                    limitProgress: 2, // slides after 2nd before/after active will have same state
                    rotate: 0,
                    slidesPerView: 1.3,
                    stretch: 0,
                    depth: 100,
                    modifier: 2.5,
                    prev: {
                      opacity: not_active_slide_opacity_value,
                      scale: not_active_slide_scale_value,
                      // will set `translateX(-90%)` on previous slides
                      translate: ["-30%", 0, 0],
                    },
                    next: {
                      opacity: not_active_slide_opacity_value,
                      scale: not_active_slide_scale_value,
                    //   will set `translateX(90%)` on next slides
                      translate: ["30%", 0, 0],
                    },
                  },

                slidesPerView: $slides_to_show,
                slidesPerGroup: $slides_to_scroll,
                loop: $loop,
                // loopFillGroupWithBlank: $loop,
                centeredSlides: $centered_slides,
                direction: $direction,
                speed: $speed,
                spaceBetween: $space_between,

                mousewheel: $mouse_wheel_scroll,

                speed: 600,
                parallax: true,
            }

            // Update breakpoints
            const $responsiveSettings = $carouselSettings['responsive'];
            const $responsiveData = {};
            $.each($responsiveSettings, function (index, value) {
                $responsiveData[value.breakpoint] = {
                    slidesPerView: value.toshow,
                    slidesPerGroup: value.toscroll
                };
            });
            swiperOptions['breakpoints'] = $responsiveData;


            // Arrow pagination
            if ($arrows) {
                swiperOptions.navigation = {
                    prevEl: '.wdt-arrow-pagination-prev-'+$moduleId,
                    nextEl: '.wdt-arrow-pagination-next-'+$moduleId
                };
            }

            // Other pagination
            if ($pagination != '') {
                if( $pagination == 'scrollbar' ) {
                    swiperOptions.scrollbar = {
                        el: '.wdt-swiper-scrollbar-'+$moduleId,
                        type: $pagination,
                        hide: true
                    };
                } else {
                    swiperOptions.pagination = {
                        el: '.wdt-swiper-pagination-'+$moduleId,
                        type: $pagination,
                        clickable: true
                    };
                }
            }

             // Autoplay direction
             $reversedirection = false;
             if($autoplay_direction == 'right') {
                 $reversedirection = true;
             }

            // Autoplay
            if ($autoplay) {
                swiperOptions.autoplay = {
                    delay: $autoplay_speed,
                    disableOnInteraction: $pause_on_interaction,
                    reverseDirection: $reversedirection,
                };
            }

            const swiperGallery = new Swiper('#'+$swiperUniqueId, swiperOptions);

            if($direction == 'vertical' && $unequal_height_compatability) {
                swiperGallery.on('slideChangeTransitionStart', function () {
                    const height = parseInt($swiperItem.find('.swiper-slide.swiper-slide-active .wdt-content-item').height(), 10) + 20;
                        $swiperWrapper.animate({height:height}, 400);
                });
            }

            // On slide change
            swiperGallery.on('slideChangeTransitionStart', function () {
                // Overflow Opacity
                if($overflow_opacity) {
                    $scope.find('.swiper').css({'overflow': 'visible'});
                    $scope.find('.swiper-slide').css({'opacity': 0.5});
                    $scope.find('.swiper-slide.swiper-slide-active').css({'opacity': 1});
                    $scope.find('.swiper-slide.swiper-slide-active').nextAll('*:lt('+(+$slides_to_show-1)+')').css({'opacity': 1});
                }
            });
            // Overflow Opacity
            if($overflow_opacity) {
                $scope.find('.swiper').css({'overflow': 'visible'});
                $scope.find('.swiper-slide').css({'opacity': 0.5});
                $scope.find('.swiper-slide.swiper-slide-active').css({'opacity': 1});
                $scope.find('.swiper-slide.swiper-slide-active').nextAll('*:lt('+(+$slides_to_show-1)+')').css({'opacity': 1});
            }

            setTimeout( function() {
                $scope.find('.swiper-slide-duplicate .elementor-invisible').removeClass('elementor-invisible');
            }, 400 );

        }, 400 );

    };

	$(window).on('elementor/frontend/init', function () {

		elementorFrontend.hooks.addAction('frontend/element_ready/wdt-advanced-carousel.default', wdtCarouselWidgetHandler);
		elementorFrontend.hooks.addAction('frontend/element_ready/wdt-counter.default', wdtCarouselWidgetHandler);
		elementorFrontend.hooks.addAction('frontend/element_ready/wdt-icon-box.default', wdtCarouselWidgetHandler);
		elementorFrontend.hooks.addAction('frontend/element_ready/wdt-instagram.default', wdtCarouselWidgetHandler);
		elementorFrontend.hooks.addAction('frontend/element_ready/wdt-team.default', wdtCarouselWidgetHandler);
		elementorFrontend.hooks.addAction('frontend/element_ready/wdt-testimonial.default', wdtCarouselWidgetHandler);
		elementorFrontend.hooks.addAction('frontend/element_ready/wdt-image-box.default', wdtCarouselWidgetHandler);
		elementorFrontend.hooks.addAction('frontend/element_ready/wdt-events.default', wdtCarouselWidgetHandler);
        elementorFrontend.hooks.addAction('frontend/element_ready/wdt-donations.default', wdtCarouselWidgetHandler);

  	});

  })(jQuery);