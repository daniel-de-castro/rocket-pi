import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server

# PAGE based on ec-og.com

PAGE="""\

<!DOCTYPE html>
<!--[if lt IE 7 ]><html class="ie ie6" lang="en"> <![endif]-->
<!--[if IE 7 ]><html class="ie ie7" lang="en"> <![endif]-->
<!--[if IE 8 ]><html class="ie ie8" lang="en"> <![endif]-->
<!--[if (gte IE 9)|!(IE)]><!--><html lang="en"> <!--<![endif]-->
<head>

<!-- Meta Tags -->
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta charset="utf-8">
<title>PiX</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="keywords" content="Subsea power, subsea energy, subsea batteries, subsea battery, renewable energy, energy storage, battery storage, clean energy, decarbonization, halo, powerhub, subsea power hub, power hub, oil & gas, subsea, energy transition, emission free, zero emission, low carbon, carbon free, blue economy" />
<meta name="description" content="Subsea energy storage and remote power generation for the energy transition, low carbon offshore operations and zero emission hydrocarbon production." />
<meta name="author" content=""/>
<meta name="format-detection" content="telephone=no">

<!-- Google / Search Engine Tags -->
<meta itemprop="name" content="EC-OG">
<meta itemprop="description" content="Subsea energy storage and remote power generation for the energy transition, low carbon offshore operations and zero emission hydrocarbon production.">
<meta itemprop="image" content="https://ec-og.com/wp-content/themes/ecog_theme/assets/img/constants/ecog-social-card.png">

<!-- Facebook Meta Tags -->
<meta property="og:type" content="website">
<meta property="og:title" content="EC-OG">
<meta property="og:description" content="Subsea energy storage and remote power generation for the energy transition, low carbon offshore operations and zero emission hydrocarbon production.">
<meta itemprop="image" content="https://ec-og.com/wp-content/themes/ecog_theme/assets/img/constants/ecog-social-card.png">

<!-- Twitter Meta Tags -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="EC-OG">
<meta name="twitter:description" content="Subsea energy storage and remote power generation for the energy transition, low carbon offshore operations and zero emission hydrocarbon production.">
<meta itemprop="image" content="https://ec-og.com/wp-content/themes/ecog_theme/assets/img/constants/ecog-social-card.png">

<!-- Mobile Specific -->
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<link rel="shortcut icon" href="" />

  
<link rel='dns-prefetch' href='//cdnjs.cloudflare.com' />
<link rel='dns-prefetch' href='//cdn.jsdelivr.net' />
<link rel='dns-prefetch' href='//use.typekit.net' />
<link rel='dns-prefetch' href='//fonts.googleapis.com' />
<link rel='dns-prefetch' href='//cdn.iconmonstr.com' />
<link rel='dns-prefetch' href='//s.w.org' />
<!-- This site uses the Google Analytics by ExactMetrics plugin v6.0.2 - Using Analytics tracking - https://www.exactmetrics.com/ -->
<script type="text/javascript" data-cfasync="false">
  var em_version         = '6.0.2';
  var em_track_user      = true;
  var em_no_track_reason = '';
  
  var disableStr = 'ga-disable-UA-43673350-1';

  /* Function to detect opted out users */
  function __gaTrackerIsOptedOut() {
    return document.cookie.indexOf(disableStr + '=true') > -1;
  }

  /* Disable tracking if the opt-out cookie exists. */
  if ( __gaTrackerIsOptedOut() ) {
    window[disableStr] = true;
  }

  /* Opt-out function */
  function __gaTrackerOptout() {
    document.cookie = disableStr + '=true; expires=Thu, 31 Dec 2099 23:59:59 UTC; path=/';
    window[disableStr] = true;
  }

  if ( 'undefined' === typeof gaOptout ) {
    function gaOptout() {
      __gaTrackerOptout();
    }
  }
  
  if ( em_track_user ) {
    (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    })(window,document,'script','//www.google-analytics.com/analytics.js','__gaTracker');

window.ga = __gaTracker;    __gaTracker('create', 'UA-43673350-1', 'auto');
    __gaTracker('set', 'forceSSL', true);
    __gaTracker('send','pageview');
    __gaTracker( function() { window.ga = __gaTracker; } );
  } else {
    console.log( "" );
    (function() {
      /* https://developers.google.com/analytics/devguides/collection/analyticsjs/ */
      var noopfn = function() {
        return null;
      };
      var noopnullfn = function() {
        return null;
      };
      var Tracker = function() {
        return null;
      };
      var p = Tracker.prototype;
      p.get = noopfn;
      p.set = noopfn;
      p.send = noopfn;
      var __gaTracker = function() {
        var len = arguments.length;
        if ( len === 0 ) {
          return;
        }
        var f = arguments[len-1];
        if ( typeof f !== 'object' || f === null || typeof f.hitCallback !== 'function' ) {
          console.log( 'Not running function __gaTracker(' + arguments[0] + " ....) because you are not being tracked. " + em_no_track_reason );
          return;
        }
        try {
          f.hitCallback();
        } catch (ex) {

        }
      };
      __gaTracker.create = function() {
        return new Tracker();
      };
      __gaTracker.getByName = noopnullfn;
      __gaTracker.getAll = function() {
        return [];
      };
      __gaTracker.remove = noopfn;
      window['__gaTracker'] = __gaTracker;
      window.ga = __gaTracker;    })();
    }
</script>
    <style type="text/css">
img.wp-smiley,
img.emoji {
  display: inline !important;
  border: none !important;
  box-shadow: none !important;
  height: 1em !important;
  width: 1em !important;
  margin: 0 .07em !important;
  vertical-align: -0.1em !important;
  background: none !important;
  padding: 0 !important;
}
</style>
  <link rel='stylesheet' id='wp-block-library-css'  href='https://ec-og.com/wp-includes/css/dist/block-library/style.min.css?ver=5.3.2' type='text/css' media='all' />
<link rel='stylesheet' id='contact-form-7-css'  href='https://ec-og.com/wp-content/plugins/contact-form-7/includes/css/styles.css?ver=5.1.7' type='text/css' media='all' />
<link rel='stylesheet' id='cookie-consent-style-css'  href='https://ec-og.com/wp-content/plugins/uk-cookie-consent/assets/css/style.css?ver=5.3.2' type='text/css' media='all' />
<link rel='stylesheet' id='style-css-css'  href='https://ec-og.com/wp-content/themes/ecog_theme/style.css?ver=1.1' type='text/css' media='all' />
<link rel='stylesheet' id='app-css-min-css'  href='https://ec-og.com/wp-content/themes/ecog_theme/assets/css/app.css?ver=1.1' type='text/css' media='all' />
<link rel='stylesheet' id='typekit-css'  href='https://use.typekit.net/owh5ggq.css?ver=1.1' type='text/css' media='all' />
<link rel='stylesheet' id='google-font-css'  href='https://fonts.googleapis.com/icon?family=Material+Icons&#038;ver=1.1' type='text/css' media='all' />
<link rel='stylesheet' id='monster-icon-css'  href='https://cdn.iconmonstr.com/1.3.0/css/iconmonstr-iconic-font.min.css?ver=1.1' type='text/css' media='all' />
<link rel='stylesheet' id='animsition-min-css'  href='https://cdnjs.cloudflare.com/ajax/libs/animsition/4.0.2/css/animsition.min.css?ver=1.1' type='text/css' media='all' />
<link rel='stylesheet' id='slick-slider-min-css'  href='https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.9.0/slick.min.css?ver=1.1' type='text/css' media='all' />
<link rel='stylesheet' id='tiny-slider-css'  href='https://cdnjs.cloudflare.com/ajax/libs/tiny-slider/2.9.2/tiny-slider.css?ver=1.1' type='text/css' media='all' />
<script type='text/javascript' src='https://ec-og.com/wp-includes/js/jquery/jquery.js?ver=1.12.4-wp'></script>
<script type='text/javascript' src='https://ec-og.com/wp-includes/js/jquery/jquery-migrate.min.js?ver=1.4.1'></script>
<script type='text/javascript'>
/* <![CDATA[ */
var exactmetrics_frontend = {"js_events_tracking":"true","download_extensions":"zip,mp3,mpeg,pdf,docx,pptx,xlsx,rar","inbound_paths":"[{\"path\":\"\\\/go\\\/\",\"label\":\"affiliate\"},{\"path\":\"\\\/recommend\\\/\",\"label\":\"affiliate\"}]","home_url":"https:\/\/ec-og.com","hash_tracking":"false"};
/* ]]> */
</script>
<script type='text/javascript' src='https://ec-og.com/wp-content/plugins/google-analytics-dashboard-for-wp/assets/js/frontend.min.js?ver=6.0.2'></script>
<link rel='https://api.w.org/' href='https://ec-og.com/wp-json/' />
<link rel="EditURI" type="application/rsd+xml" title="RSD" href="https://ec-og.com/xmlrpc.php?rsd" />
<link rel="wlwmanifest" type="application/wlwmanifest+xml" href="https://ec-og.com/wp-includes/wlwmanifest.xml" /> 
<meta name="generator" content="WordPress 5.3.2" />
<link rel="canonical" href="https://ec-og.com/" />
<link rel='shortlink' href='https://ec-og.com/' />
<link rel="alternate" type="application/json+oembed" href="https://ec-og.com/wp-json/oembed/1.0/embed?url=https%3A%2F%2Fec-og.com%2F" />
<link rel="alternate" type="text/xml+oembed" href="https://ec-og.com/wp-json/oembed/1.0/embed?url=https%3A%2F%2Fec-og.com%2F&#038;format=xml" />
<style id="ctcc-css" type="text/css" media="screen">
        #catapult-cookie-bar {
          box-sizing: border-box;
          max-height: 0;
          opacity: 0;
          z-index: 99999;
          overflow: hidden;
          color: #ffffff;
          position: fixed;
          left: 0;
          bottom: 0;
          width: 100%;
          background-color: #0e1117;
        }
        #catapult-cookie-bar a {
          color: #fff;
        }
        #catapult-cookie-bar .x_close span {
          background-color: #ffffff;
        }
        button#catapultCookie {
          background:#171b24;
          color: #ffffff;
          border: 0; padding: 6px 9px; border-radius: 3px;
        }
        #catapult-cookie-bar h3 {
          color: #ffffff;
        }
        .has-cookie-bar #catapult-cookie-bar {
          opacity: 1;
          max-height: 999px;
          min-height: 30px;
        }</style>
<!-- Favicon -->
<link rel="icon" type="image/x-icon" href="https://www.spacex.com/sites/all/themes/spacex2012/favicon.ico">
<link rel="apple-touch-icon" href="https://ec-og.com/wp-content/themes/ecog_theme/assets/img/favicon/apple-touch-icon.png">
<link rel="apple-touch-icon" sizes="72x72" href="https://ec-og.com/wp-content/themes/ecog_theme/assets/img/favicon//apple-touch-icon-72x72.png">
<link rel="apple-touch-icon" sizes="114x114" href="https://ec-og.com/wp-content/themes/ecog_theme/assets/img/favicon/apple-touch-icon-114x114.png">
<link rel="apple-touch-icon" sizes="57x57" href="https://ec-og.com/wp-content/themes/ecog_theme/assets/img/favicon/apple-icon-57x57.png">
<link rel="apple-touch-icon" sizes="60x60" href="https://ec-og.com/wp-content/themes/ecog_theme/assets/img/favicon/apple-icon-60x60.png">
<link rel="apple-touch-icon" sizes="72x72" href="https://ec-og.com/wp-content/themes/ecog_theme/assets/img/favicon/apple-icon-72x72.png">
<link rel="apple-touch-icon" sizes="76x76" href="https://ec-og.com/wp-content/themes/ecog_theme/assets/img/favicon/apple-icon-76x76.png">
<link rel="apple-touch-icon" sizes="114x114" href="https://ec-og.com/wp-content/themes/ecog_theme/assets/img/favicon/apple-icon-114x114.png">
<link rel="apple-touch-icon" sizes="120x120" href="https://ec-og.com/wp-content/themes/ecog_theme/assets/img/favicon/apple-icon-120x120.png">
<link rel="apple-touch-icon" sizes="144x144" href="https://ec-og.com/wp-content/themes/ecog_theme/assets/img/favicon/apple-icon-144x144.png">
<link rel="apple-touch-icon" sizes="152x152" href="https://ec-og.com/wp-content/themes/ecog_theme/assets/img/favicon/apple-icon-152x152.png">
<link rel="apple-touch-icon" sizes="180x180" href="https://ec-og.com/wp-content/themes/ecog_theme/assets/img/favicon/apple-icon-180x180.png">
<link rel="icon" type="image/png" sizes="192x192"  href="https://ec-og.com/wp-content/themes/ecog_theme/assets/img/favicon/android-icon-192x192.png">
<link rel="icon" type="image/png" sizes="32x32" href="https://ec-og.com/wp-content/themes/ecog_theme/assets/img/favicon/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="96x96" href="https://ec-og.com/wp-content/themes/ecog_theme/assets/img/favicon/favicon-96x96.png">
<link rel="icon" type="image/png" sizes="16x16" href="https://ec-og.com/wp-content/themes/ecog_theme/assets/img/favicon/favicon-16x16.png">
    
<!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
<!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
<!--[if lt IE 9]>
<script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
<script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
<![endif]-->

<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-43673350-1"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());

gtag('config', 'UA-43673350-1');
</script>

</head>

<body class="home page-template page-template-front-page page-template-front-page-php page page-id-6">
  
<!--div class="animsition">
  
  <div class="loading-screen">
    <div id="lottie"></div>
  </div>

<div class="search-overlay">
  <button class="search-close">
    <i class="material-icons">close</i>
  </button>
  <form class="search-bar" action="/" method="get">
    <input type="search" name="s" autocomplete="off" id="siteSearch" value="" placeholder="Type to search..."/>
    <button class="search-submit">
      <i class="material-icons">search</i>
    </button>
  </form>
</div>

<div class="menu-overlay">
  <div class="menu-mask"></div>
  <div class="menu">
    <div class="inner">
      <div class="header">
        <a class="logo" href="/">
          <svg xmlns="http://www.w3.org/2000/svg" width="39" height="36" viewBox="0 0 39 36">
            <g transform="translate(-125.697 -12)">
              <path d="M516.1,43.093a9.234,9.234,0,0,1,5.716-3.263h.013c.276-.015.539-.022.785-.02h.091c.1-.018.2-.036.3-.052a33.478,33.478,0,0,0-10.237.544,43.058,43.058,0,0,1-13.2.263,75.154,75.154,0,0,1-10.543-2.477s-4.936-1.478-1.8,3.309a8.4,8.4,0,0,0,5.518,2.972,36.242,36.242,0,0,0,13.564.039A78.774,78.774,0,0,1,516.1,43.093Z" transform="translate(-360.153 -25.873)" fill="#12a5df"/>
              <path d="M513.55,66.372a9.442,9.442,0,0,1,0,6.631l-.006.012c-.123.249-.247.485-.369.7l-.045.079c-.034.1-.068.194-.1.292a34.257,34.257,0,0,0,4.565-9.27,44.08,44.08,0,0,1,6.263-11.733,76.34,76.34,0,0,1,7.321-8.053s3.7-3.614-1.965-3.214c0,0-2.738.228-5.276,3.392a37.014,37.014,0,0,0-6.7,11.908A80.728,80.728,0,0,1,513.55,66.372Z" transform="translate(-367.668 -26.94)" fill="#8ec541"/>
              <path d="M492.018,46.619a9.256,9.256,0,0,1-5.645-3.387l-.007-.012c-.15-.234-.287-.462-.407-.677l-.045-.081c-.066-.079-.131-.158-.2-.239a34.2,34.2,0,0,0,5.555,8.7,43.972,43.972,0,0,1,6.784,11.434,77.147,77.147,0,0,1,3.112,10.471s1.183,5.061,3.74-.063c0,0,1.206-2.493-.189-6.314a37.076,37.076,0,0,0-6.708-11.906A80.219,80.219,0,0,1,492.018,46.619Z" transform="translate(-360.023 -27.059)" fill="#3b3d43"/>
            </g>
          </svg>
        </a>
        <button class="menu-close">
          <i class="material-icons">close</i>
        </button>
      </div>
      <nav>
        <ul id="menu-primary-menu" class="nav-primary"><li id="menu-item-159" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-159"><a title="Products" href="https://ec-og.com/products/">Products</a></li>
<li id="menu-item-160" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-160"><a title="Research &amp; Development" href="https://ec-og.com/development/">Research &#038; Development</a></li>
</ul>       <ul id="menu-secondary-menu" class="nav-secondary"><li id="menu-item-166" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-166"><a title="About" href="https://ec-og.com/about/">About</a></li>
<li id="menu-item-165" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-165"><a title="Newsroom" href="https://ec-og.com/newsroom/">Newsroom</a></li>
<li id="menu-item-167" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-167"><a title="Contact" href="https://ec-og.com/contact/">Contact</a></li>
</ul>     </nav>
      <div class="footer">&copy; 2020 EC-OG. All Rights Reserved.</div>
    </div>
  </div>
</div-->

<header class="site-header px-container" height="200">
  <div class="inner">
    <div>
      <a class="logo" href="/">
        <img src="https://www.spacex.com/sites/spacex/files/spacex_logo_white.png" width="200" height="20" style="display: inline-block"/>
      </a>   
    </div>
    <div>
      <ul id="menu-secondary-menu-1" class="nav-secondary">
        <li class="menu-item menu-item-type-post_type menu-item-object-page menu-item-166"><a title="About" href="#aboutSlides">About</a></li>
        <li class="menu-item menu-item-type-post_type menu-item-object-page menu-item-165"><a title="Github" href="https://github.com/daniel-de-castro/PiX">Github</a></li>
      </ul>
      <!--button class="search-toggle">
        <i class="material-icons">search</i>
      </button>
      <button class="menu-toggle">
        <i class="material-icons">menu</i>
      </button-->
    </div>
  </div>
</header>
<div class="px-container bg-black home-hero-container">
    <div id="particles-js"></div>
      <div class="hero-image show-for-large" style="background-image:url('https://spacex.com/sites/all/themes/spacex2012/images/falcon9/header___falcon%209.jpg')"></div>
        <div class="hero-image hide-for-large" style="background-image:url('https://spacex.com/sites/all/themes/spacex2012/images/falcon9/header___falcon%209.jpg')"></div>
        <div class="grid-container">
        <div class="home-hero">
            <div>
                <h1 class="t-demi white hero-title">PiRocket</h1>
                <p class="white m-0 hero-message">Telemetry live streaming for space flight</p>
            </div>
        </div>
    </div>
    <a class="hero-arrow scroll-trigger">
        <i class="material-icons">keyboard_arrow_down</i>
    </a>
</div>
      
  <div class="split-section bg-white">
      <div class="image"><img src="stream.mjpg" width="680" height="500" style="display: inline-block"/></div>
      <div class="content">
          <div class="inner">
              <p>Telemetry will be here</p>
              <p>Information like altitude, pressure, temperature, humidity, accelerometer and gyroscope shall be displayed nicely in here.</p>
              <a class="btn btn-primary">And we can make it pretty</a>
          </div>
      </div>
  </div>

  <div class="home-products-container" id="aboutSlides" height="800">
      <div class="home-products">
                    <div>
                <div class="slide">
                    <div class="image" style="background-image:url('https://spacex.com/sites/spacex/files/000_crew_dragon.jpg');"></div>
                    <div class="grid-container">
                        <div class="content">
                            <div class="inner">
                                <h2 class="heading">Space stations</h2>
                                <p class="message">Rendezvous to the space station effortlessly with state of the art avionics.</p>
                                <a class="btn btn-stroke""><span>More pretty CSS</span></a>
                                                                                                  </div>
                        </div>
                    </div>
                </div>
            </div>
                      <div>
                <div class="slide">
                    <div class="image" style="background-image:url('http://spacex.com/sites/spacex/files/0000_mars_landing.jpg'); transform: scaleX(-1);"></div>
                    <div class="grid-container">
                        <div class="content">
                            <div class="inner">
                                <h2 class="heading">Other worlds</h2>
                                <p class="message">The journeys to Mars and beyond shall be an experience full of awe and wonder, not just to those on board.</p>
                                <a class="btn btn-stroke" href="https://ec-og.com/development/"><span>Lambo cash bruv gang lit fam</span></a>
                                </div>
                        </div>
                    </div>
                </div>
            </div>
                </div>
  </div>
    
</body>
</html>

<script type='text/javascript'>
/* <![CDATA[ */
var wpcf7 = {"apiSettings":{"root":"https:\/\/ec-og.com\/wp-json\/contact-form-7\/v1","namespace":"contact-form-7\/v1"},"cached":"1"};
/* ]]> */
</script>
<script type='text/javascript' src='https://ec-og.com/wp-content/plugins/contact-form-7/includes/js/scripts.js?ver=5.1.7'></script>
<script type='text/javascript'>
/* <![CDATA[ */
var ctcc_vars = {"expiry":"30","method":"1","version":"1"};
/* ]]> */
</script>
<script type='text/javascript' src='https://ec-og.com/wp-content/plugins/uk-cookie-consent/assets/js/uk-cookie-consent-js.js?ver=2.3.0'></script>
<script type='text/javascript' src='https://ec-og.com/wp-content/themes/ecog_theme/assets/js/foundation/jquery.min.js?ver=1.1'></script>
<script type='text/javascript' src='https://ec-og.com/wp-content/themes/ecog_theme/assets/js/foundation/what-input.min.js?ver=1.1'></script>
<script type='text/javascript' src='https://ec-og.com/wp-content/themes/ecog_theme/assets/js/foundation/foundation.min.js?ver=1.1'></script>
<script type='text/javascript' src='https://cdnjs.cloudflare.com/ajax/libs/animsition/4.0.2/js/animsition.min.js?ver=1.1'></script>
<script type='text/javascript' src='https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.9.0/slick.min.js?ver=1.1'></script>
<script type='text/javascript' src='https://cdnjs.cloudflare.com/ajax/libs/tiny-slider/2.9.2/min/tiny-slider.js?ver=1.1'></script>
<script type='text/javascript' src='https://cdnjs.cloudflare.com/ajax/libs/mixitup/3.3.1/mixitup.js?ver=1.1'></script>
<script type='text/javascript' src='https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js?ver=1.1'></script>
<script type='text/javascript' src='https://ec-og.com/wp-content/themes/ecog_theme/assets/js/app.js?ver=1.1'></script>
<script type='text/javascript' src='https://ec-og.com/wp-content/themes/ecog_theme/assets/js/plugins/lottie.js?ver=1.1'></script>
<script type='text/javascript' src='https://ec-og.com/wp-content/themes/ecog_theme/assets/js/pages/home.js?ver=1.1'></script>
<script type='text/javascript' src='https://ec-og.com/wp-includes/js/wp-embed.min.js?ver=5.3.2'></script>
      
        <script type="text/javascript">
          jQuery(document).ready(function($){
                        if(!catapultReadCookie("catAccCookies")){ // If the cookie has not been set then show the bar
              $("html").addClass("has-cookie-bar");
              $("html").addClass("cookie-bar-bottom-bar");
              $("html").addClass("cookie-bar-bar");
                          }
                                  });
        </script>
      
      <div id="catapult-cookie-bar" class=""><div class="ctcc-inner "><span class="ctcc-left-side">This site uses cookies <a class="ctcc-more-info-link" tabindex=0 target="_blank" href="https://ec-og.com/privacy-policy/">Find out more</a></span><span class="ctcc-right-side"><button id="catapultCookie" tabindex=0 onclick="catapultAcceptCookies();">X</button></span></div><!-- custom wrapper class --></div><!-- #catapult-cookie-bar -->
<!-- Page supported by LiteSpeed Cache 2.9.9.2 on 2020-04-17 21:15:33 -->
"""

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    output = StreamingOutput()
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()
