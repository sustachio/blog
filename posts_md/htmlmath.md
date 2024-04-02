MathMl: Easy Embedded Math in HTML (No extra libraries, browser supported!)
Post
2024-3-31
Earlier today I started working on an HTML reference table for common equations used in circuits (maybe a future blog post?), but I needed a good way to format the math expressions. My first thought was to use LaTeX, but I didn't really want to put the time in to learn it. After a bit of googling, I found out about the `<math>` tag in standard HTML. It lets you write equations fully in HTML with no special parsing rules or anything.

The MathML standard has been ([kind of](https://www.peterkrautzberger.org/0186/)) supported since the 1990s and, although being a bit annoying to write, it can work in a pinch without adding any new dependencies.

The syntax is pretty simple: everything in your equation is in a `<math>` tag, all numbers are in a `<mn>` tag (for math number), all identifiers in a `<mi>`, and all operations in a `<mo>` tag.

For example, the equation <math><mi>y</mi><mo>=</mo><mi>x</mi></math> could be written as:

    <math>
        <mi>y</mi>
        <mo>=</mo>
        <mi>x<mi>
    </math> 

Although not too useful for simple equations like that, it becomes helpful when working with subscripts, exponents, fractions, square roots, and other strange-looking math things. 

Here is the capacitive reactance formula written with MathML:

    <math>
        <msub>
            <mi>X</mi>
            <mi>c</mi>
        </msub>
        <mo>=</mo>
        <mfrac>
            <mn>1</mn>
            <mrow>
                <mn>2</mn>
                <mn>&pi;</mn>
                <mi>f</mi>
                <mi>c</mi>
            </mrow>
        </mfrac>
    </math>

<math>
    <msub>
        <mi>X</mi>
        <mi>c</mi>
    </msub>
    <mo>=</mo>
    <mfrac>
        <mn>1</mn>
        <mrow>
            <mn>2</mn>
            <mn>&pi;</mn>
            <mi>f</mi>
            <mi>c</mi>
        </mrow>
    </mfrac>
</math>

Here, `<msub>` is used to represent subscripts, and `<mfrac>` for fractions. Since `<mfrac>` is only meant to work with two elements (numerator and denominator), we can use `<mrow>` to group values on the same line.

As I quickly learned, MathML can get very tedious to read and write even such short equations. This problem is very common with larger HTML projects of any kind, so it might be a good choice to use something like LaTeX for writing your equations, but MathML has the advantage of not needing to do anything else other than adding to the HTML code which makes it alright for quick and small equations.

__Side note:__ One thing I do like about HTML is the [character entities](https://www.w3schools.com/html/html_entities.asp). These allow you to write symbols not on your keyboard with the format `&name;`. For example, &times; &pi; &ohm; &Delta; &theta; could be written as `&times; &pi; &ohm; &Delta; &theta`. Before finding out about this I would just google the symbol name and copy and paste it from the first result, but this is a lot easier once you get to know some of the basic symbols.

A complete reference of MathML can be found [here](https://developer.mozilla.org/en-US/docs/Web/MathML/Element).

Anyway, I will end this article off with the MathML code for the Quadratic Formula, which took me 4 and a half minutes to write (including googling time).

    <math>
        <mi>x</mi>
        <mo>=</mo>
        <mfrac>
            <mrow>
                <mo>-</mo>
                <mi>b</mi>
                <mo>&plusmn;</mo>
                <msqrt>
                    <msup>
                        <mi>b</mi>
                        <mn>2</mn>
                    </msup>
                    <mo>-</mo>
                    <mn>4</mn>
                    <mi>a</mi>
                    <mi>c</mi>
                </msqrt>
            </mrow>
            <mrow>
                <mn>2</mn>
                <mi>a</mi>
            </mrow>
        </mfrac>
    </math>

<math>
    <mi>x</mi>
    <mo>=</mo>
    <mfrac>
        <mrow>
            <mo>-</mo>
            <mi>b</mi>
            <mo>&plusmn;</mo>
            <msqrt>
                <msup>
                    <mi>b</mi>
                    <mn>2</mn>
                </msup>
                <mo>-</mo>
                <mn>4</mn>
                <mi>a</mi>
                <mi>c</mi>
            </msqrt>
        </mrow>
        <mrow>
            <mn>2</mn>
            <mi>a</mi>
        </mrow>
    </mfrac>
</
