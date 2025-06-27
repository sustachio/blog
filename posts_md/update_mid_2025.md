Updates and Future of the Blog
Post
2025-6-20
Hello! It's been a while since I've posted on this blog (or since its been online, I keep forgetting to renew the SSL certificate :p), but I do wish to keep this blog more active from now on. I will be posting about older projects that never made it here and any new things I find or make! This post will serve just as a quick update to what I've been up to and discuss the future of the blog.

A lot has changed since the last post, I have been researching electronics a good bit and have gotten into ham radio (look for KJ5EBW on the air!). Most of my effort has been put towards working on synthesizers for electronic music, but I also have a couple odd projects I'd like to post about.

**Radio**

I've been having lots of fun with ham radio, mainly just odd Parks on the Air (POTA) activations whenever I have a chance. If you're not aware, POTA is a awards program which encourages praticipants to go out and set up their radios in state or national parks/memorials and try to talk to people from wherever! I've been putting together my own small station that I can setup just about anywhere currently consisting of a G90 radio, a [12V 12Ah LiFePO4 battery](https://www.amazon.com/XZNY-12V-LiFePO4-Lithium-Battery/dp/B0D9Y9VDH8/ref=sr_1_24?crid=3M4ZHP2ODTR0G&dib=eyJ2IjoiMSJ9.v_r5SXrdXMqJ4Pk45VHFjP056myxQMvdq5SAvZvenSeCYdqjnbvujiyLXD5Gaeye4cPncdGnWYNAk3LkTDbZ--UjyRII1La9SDDMUEo5fyTHmBc9UiyJRda4YZNMl9xHd_Fv1KbdOcKCVGbpd2yyaJFjkDXcQPNtYNXx-lU0JnX9_yGJN3l17yxab_BT1wx3LwYTaQXz4QfZeTq1lsdHT_R3ct8ZouMfgUOYPRPqO_k1aSTtq3iYtPqgvfX5yLyyq5BvbtF_rR5ki6O8y2d2maGkzQqjQrkJQtVOLAsN3Lk.IOHemHy13bCpBaGCXvu4txLqI72YMak2QtHoR3EqsbA&dib_tag=se&keywords=lifepo4%2B12v&qid=1750471802&sprefix=lifepo%2B12%2Caps%2C192&sr=8-24&th=1), a [10m tall spiderbeam telescopic fiberglass mast](https://www.spiderbeam.com/product_info.php?info=p428_Spiderbeam%2010m%20Mini%20fiberglass%20pole.html&XTCsid=526bb0c3cc95af3c5e8954ac0604457a) (this thing packs down to like 2 ft and is only about 4 pounds its awesome), and a simple wire verticle antenna for 40m. Each wire for the verticle (5 in total, 4 for a ground plane) is split up in 2 places by wire terminals with a screw through them attaching the two sides of the wire so I can take segments off to make it a 20m or 10m antenna when needed. I also own a [UV-K5 VHF/UHF radio](https://www.amazon.com/QUANSHENG-UV-K5-Rechargeable-Emergency-Receiver/dp/B0C9TVSYYM) which has had its problems (post on this later), but works well for hitting local repeaters and was only $30.

I initially got into the hobby through my schools club, K5LBJ, which has unfortunately been slowly decreasing in size after the ham radio class at our school ended as the teacher left. I joined about a year and a half ago. I was lended a 10m radio and power supply and built my own dipole which I strung up between a basketball hoop and tetherball pole in my backyard. The setup was pretty easy and worked well for a while, but the power supply was limited to being near an outlet, so I inevitably invested in a battery and also just decided to get a G90 (a rather nice and small software defined radio) as I was having lots of fun with HF radio.

With the portable setup I was able to activate Perdinalles Falls State Park, Rocky Mountain National Park, and a couple of other state parks. When I went to Rocky Mountain National Park, I only had my technician  license which only allowed me to transmit on 10m, but at the time the propagation was bad and I couldn't hear anyone on 10m. I had been studying for my general license (which allows me to transmit just about anywhere on the ham bands), and decided to just do an online test while still in Colorado as I really wanted that activation. I managed to get it (pictures below) on 20m with an extended dipole I had thrown together with some twisty wire connectors, duct tape, and some extra wire from the local hardware store.

After a few more attempted activations in smaller parks around Texas, I realized that there were many times that there was simply no good place to put up a dipole (usually no trees in sight), so I decided to invest in the 10m spiderbeam mast mentioned above to be able to deploy anywhere. This allowed me to get an activation at Ink's Lake State Park while camping overnight. I am yet to actually get a contact with the full 40m antenna, but have been having lots of luck on 20m and 10m. I actually managed to get all of the required 10 contacts for an activation only with Park to Park contacts where you talk with someone also doing Parks on the Air at a park, but talked with a few other folks after. I had been hearing a lot of people calling out in the Extra class only portion of the band, so I decided to start studying for that and managed to get it on April 19th 2025.

<div class="picture-grid">
    <div>
        <img src="{{ url_for('static', filename='radio_pics_update/perdenales.jpg') }}" alt="Radio at perdenales state park" />
        <i>Radio at Perdenales State Park</i>
    </div>

    <div>
        <img src="{{ url_for('static', filename='radio_pics_update/rocky_chair.jpg') }}" />
        <i>Setup at Rocky Mountain</i>
    </div>

    <div>
        <img src="{{ url_for('static', filename='radio_pics_update/rocky_dipole.jpg') }}" />
        <i>Dipole at Rocky Mountain</i>
    </div>

    <div>
        <img src="{{ url_for('static', filename='radio_pics_update/mkinney_g90_tower.jpg') }}" />
        <i>Radio at McKinney Falls (G90 tower, mine is the one with the rubber duck knob on the top)</i>
    </div>

    <div>
        <img src="{{ url_for('static', filename='radio_pics_update/inks_lake.jpg') }}" />
        <i>Night Radio at Ink's Lake (Spidebeam mast at half height or so)</i>
    </div>

    <div>
        <img src="{{ url_for('static', filename='radio_pics_update/fish_place.jpg') }}" />
        <i>Radio at Red River Fish Hatchery (very tricky spot, set up dipole perpendicular in valley, took over an hour to get 10 contacts)</i>
    </div>
</div>

If you live in Austin and are interested in getting licensed or just checking the hobby out, the [N5OAK club](https://n5oak.org/) has quarterly meetings where anyone is welcome and testing after each meeting. I tested for both my Technician and Extra class licences there and had a very good experience. Also for studying for the licence, ARRL has some good licensing manuals on amazon for each class and the site <https://hamstudy.org/> is very useful once you've got the concepts down and just need to review.

**Electronics**

I picked up an interest in analog electronics while trying to learn how to better take advantage of microcontrollers and make actual physical projects instead of just coding things, but I found the pure analog side very interesting. I got a copy of Electronics for Dummies which was pretty basic but a good intro and later downloaded a pdf of The Art of Electronics, which I absolutely loved, to read while on break at work. I eventually got a physical copy of the book and went through the first half throughout last summer.

I have a friend from my school's radio club (Lucas, KI5ZWV) who was interested in building synthesizers for making electronic music, so I thought I would give that a try as a way to apply what I was learning. So far I've been mainly working on a modular synthesizer (only 3 modules down so far) and a few standalone things like an atari punk console pcb, keyboard that fits in a Altoids tin, and a abstract electronic self portrait thing for English class (will post about all of these). I've also done some guitar pedal repair for my dad and one of his friends and have repaired my handheld radio at least twice now.

A bit more random but I also picked up this old portable TV from an antique store which I put some adapters on to be able to use it as a monitor. It was a bit funny because it only takes RF input from an antenna so I had to get a AV to NTSC converter and an HDMI to AV adapter and then tune into channel 4 to get a signal.

<div class="picture-grid">
    <div>
        <img src="{{ url_for('static', filename='radio_pics_update/modular_2_one_half_front.jpg') }}" />
        <i>Front panel of the start of my modular synth, so far a VCO, an Attenuverter, and a VCF (lettering not yet etched in front) (separate +/-12V module)</i>
    </div>

    <div>
        <img src="{{ url_for('static', filename='radio_pics_update/modular_2_one_half.jpg') }}" />
        <i>Back side of the synth</i>
    </div>

    <div>
        <img src="{{ url_for('static', filename='radio_pics_update/old_tv_csgo.jpg') }}" />
        <i>CSGO 2 on the old TV</i>
    </div>
</div>

**Blog Future**

I'm going to try and be more active about posting projects and such and will also try and post many of the projects I have worked on in the past. I want this site to be able to serve to document any projects I make and my progress learning electronics or what every else I get involved with.

I'm looking forwards to writing more! Have a good day.
