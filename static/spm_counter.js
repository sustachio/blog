last_stroke_time = 0
stroke_length_average = 0
strokes_counted = 0

function reset() {
    last_stroke_time = 0
    stroke_length_average = 0
    strokes_counted = 0

    update_ui()
}

function stroke() {
    time = Date.now()

    // break if first stroke (no reference)
    if (last_stroke_time == 0) {
        last_stroke_time = time
        return
    }

    stroke_length = Date.now() - last_stroke_time

    // update the average
    stroke_length_average = 
        ((stroke_length_average * strokes_counted) + stroke_length) /
        (strokes_counted + 1)

    strokes_counted += 1
    last_stroke_time = time

    update_ui()
}

function update_ui() {
    strokes_per_minuete = 60/(stroke_length_average/1000)
    strokes_per_minuete = Math.round(strokes_per_minuete * 10) / 10 // one decimal point

    if (strokes_per_minuete > 100000 || strokes_per_minuete < 0) {
        strokes_per_minuete = 0
    }

    $("#spm").text(strokes_per_minuete)
}