RISC Processor, Custom ISA, and compiler
Project
2026-4-4
Over spring break, I put together a simple 32 bit RISC (reduced instruction set computer) processor using Logisim in order to follow along with the architecture described in the book *Computer Architecture: A Quantitative Approach*. Since the goal was primarily to study higher level computer architecture, not every component was built from logic gates and I made heavy use of the built in multiplexers. To have something to run on the processor, I also wrote a compiler for a custom object oriented programming language which compiles down to an intermediate language based on the stack based VM from the *Nand2Tetris* series. I implemented a second compiler which will go from this intermediate language down to my own assembly language.

<table>
    <tr>
        <td>
            <img src="{{ url_for('static', filename='rrisc/screen.png') }}"></img>
            <i>Current state of the processor. Here it ran a very unoptimized program to display red and green gradients on the x and y axes of the screen which took about 200 cycles per pixel (lots from preparing memory mapped IO data)</i>
        </td>
    </tr>
    <tr>
        <td>
            <img src="{{ url_for('static', filename='rrisc/isa.png') }}"></img>
            <i>Current ISA from the spreadsheet on the GitHub page.</i>
        </td>
    </tr>
</table>

This project is most certainly not finished and I would like to continue to add onto it as I continue to go through the book. The compiler also has basically no optimization as of now and I look forward to making it more efficient.

Most of the project is documented on its GitHub page ([https://github.com/sustachio/reduced-reduced-instruction-set-computer-and-compiler](https://github.com/sustachio/reduced-reduced-instruction-set-computer-and-compiler)), so not everything will be discussed here. Nonetheless, the basic features include:

- A 5 stage pipeline (instruction fetch, instruction decode / register read, execute, memory read/write, and register writeback)
- Register forwarding/bypassing - will automatically pull needed data from later pipeline stages if it has not yet been written to registers reducing stalls
- 32 registers
- 28 opcodes implemented (ISA will allow for up to 64, will likely add more)
- Memory mapped IO (currently just a screen but easy to extend)

No speculative branch prediction has been implemented yet so the compiler must insert 3 nops after each jump or conditional branch to prevent instructions following a successful jump in memory from being executed.

## Rubellite programming language

I've always wanted to write a compiler from scratch and this project seemed like the perfect excuse to do so. The language (which I've dubbed `rubellite` from a cheaper version of rubies) is a really weird combination of Java, Ruby, and Swift. I wanted to try to make something new and many of the choices made early on ended up being not so good but I am still proud I got something to work. As an example of some of the code, here is a very early version of heap management I threw together to test memory access (just use as a syntax example, I am aware it is uncomplete):

    class Memory
        static int heapptr;

        staticdef int Init()
            let $heapptr = 30000;
        end

        staticdef int alloc(int size)
            local int newpos;

            let $heapptr[0] = size;
            let newpos = $heapptr - size;
            let $heapptr = $heapptr - size - 1;

            return newpos;
        end
    end

In this example, `$` is used to access static variables and `.` would be used to access object fields. All locals must be declared at the start of a function or method. If other classes or objects were referenced you could use `ClassName$staticfuncName()` or `ObjectName.methodName()` to call their functions or methods. For now, all functions and methods are public and all static variables and fields can be publicly accessed, but you must write setter methods if you want to change them outside of the scope of an object.

Although not demonstrated here, you can have `if (...) then ... [else ...] end` and `while (...) do ... end` statements. Right now all functions and methods must be contained within a class, but I may change this in the future.

The language itself is tokenized and then parsed into an abstract syntax tree. This then compiles down to a slightly modified version of the intermediate language from the *Nand2Tetris* series which is just a stack based VM. Since I wrote all of the code to manage function calls and returns on the stack when implementing the intermediate language, it made the full language much easier to write. I will likely move away from this intermediate language and go straight to assembly as it is proving to make it more difficult to optimize the compiler.

## Final remarks

I'm looking forwards to expanding this processor and potentially reworking it to allow for some sort of instruction scheduling. There is a full devlog on the GitHub readme, but I will include a small log for changes made to this article here.

- 4/4/2026 - Initial blog post

If you are looking to learn about some computer architecture, I'd strongly recommend you also read *Computer Architecture: A Quantitative Approach*, as it has proven to be a very in-depth and informative text. The processor in the initial version of this post is just based on the content in Appendix C which was just a review of pipelined processors.

Thank you for reading and have a wonderful day! ^_^
