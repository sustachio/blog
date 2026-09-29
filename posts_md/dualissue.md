Dual-Issue Out-of-Order Superscaler Processor Using Tomasulo's algorithm in Logisim
Project
5-25-2026
[Project GitHub](https://github.com/sustachio/dual-issue-lalu/tree/main)

This article discusses my implementation of Tomasulo's algorithm on a simple simulated processor in Logisim and how I was able to extend it to allow for dual-issuing of instructions. If you are unfamiliar with Tomasulo's algorithm, I'd strongly recommend checking out my [previous post](https://sethmueller.page/post/tomasulo-s-algorithm) describing the algorithm. Before I get started, here's some quick definitions of everything in the very long title:

- Dual-Issue - Two instructions are being fetched from memory each clock cycle
- Out-of-Order - Instructions can be queued up and ran out-of-order from how they appeared in the program in order to prevent stalls when one instruction takes too long but others do not depend on it. This also allows multiple instructions to be ran at the same time, given they don't depend on each other.
- Superscaler - Multiple instructions are able to be executed in each clock cycle using multiple execution units
- Tomasulo's algorithm - The process which is used to manage dependencies between instructions and determine which ones can be run and when. This will be explored throughout the course of this article.

Alright, on to the article...

After reading through some more of _Computer Architecture: A Quantitative Approach_, I got inspired to have a hand at my own implementation of Tomasulo's algorithm, which allows for processors to handle running and queueing multiple instructions at once. Once I got the basic algorithm down, it was pretty straightforward to expand the processor to be able to commit multiple instructions per clock cycle and fetch multiple instructions from memory per clock cycle (hence the "dual-issue" in the title).

As with the other simulated processor I put together ([link](https://sethmueller.page/post/risc-processor-custom-isa-and-compiler)), I used Logisim to design this whole thing and tried to keep everything else simple in order to maintain focus on the algorithm itself in the project. The ISA I implemented was from a digital electronics class my school offers and is very minimalistic (see image for description). Since jump addresses can only be 6 bits long, this limits all programs to being only 64 instructions, which makes the ISA a bit impractical, but again, the point of this was just to study the theory of instruction-level parallelism.

<img style="max-width:25rem" src="{{ url_for('static', filename='tomasoldos/laluisa.png') }}"></img>

<i>The very simple ISA. Instructions are 8-bit and operate on 4 16-bit registers.</i>


## The Processor/Implemenation in Logisim 

<img src="{{ url_for('static', filename='tomasoldos/overview.png') }}"></img>

<i>Top-level overview of the processor. You may need to open it in a new tab and zoom in to see the detailed text.</i>

Here is the root level of the entire processor where everything connects. The bulk of Tomasulo's algorithm comes from the `Reservation Stations`, the `Issue Logic`, the `Common Data Bus`, and the `Register Stats` blocks.

Since the processor is dual-issue, the `Instruction Memory` contains 16-bit words so two 8-bit instructions can be fetched each clock cycle.

Here is a basic overview of the responsiblities of each part:

- Program Counter/Instruction memory - Keeps track of where you are in the program and fetch instructions from memory. In the case that the program is fetching from an odd memory address, only the second instruction will be read in (back half of the 16-bit memory word) and the other will be served as a nop.
- Reservation stations - Hold instructions waiting to be executed/being executed and tell execution units (ALUs, Memory Controller, Branch Manager) when to execute. These must also be able to clear themselves when they see their result written on the common data bus.
- Register Stats / Registers - Keep track of which reservation station each register is waiting on and update when the relevant reservation station is seen on the common data bus.
- Issue logic - Generate data used to place instructions inside of reservation stations and manage dependancies between the two instructions being issued.
- Common data bus - Allow for up to two execution units per clock cycle to send their data down the common data bus and complete operation.

## Preformance

To demonstrate the preformance of the processor I ran the following simple endless fibonacci sequence calculator program which places fibonacci numbers starting with the second term (1, 2, 3, 5, ...) in memory consecutively.

    ldi R0,0     # current memory address to write to
    ldi R1,1     # constant 1
    ldi R2,1     # prior fibonacii value #1
    ldi R3,1     # prior fibonacci value #2
    t0: st R3,R0 # mem[R0] = R3
    add R0,R1    # R0 = R0 + 1
    add R2,R3    # R2 = R2 + R3
    st R2,R0     # mem[R0] = R2
    add R0,R1    # R0 = R0 + 1
    add R3,R2    # R3 = R3 + R2
    jmp t0       # loop

    # compiled: 0e5e 9ede cb12 b28b 12e2 1000

The time to place 46,368&mdash;the largest fibonacci number able to be represented with 16 bits&mdash;in memory for this processor and other simple ones is listed below:

<table>
    <tr>
        <th>Architecture</th>
        <th>Cycles to store 46,368</th>
        <th>Average cycles per number after setup</th>
    </tr>
    <tr>
        <td>This processor</td>
        <td>47 cycles</td>
        <td>2 cycles/num</td>
    </tr>
    <tr>
        <td>Single cycle processor</td>
        <td>82 cycles</td>
        <td>3.5 cycles/num</td>
    </tr>
    <tr>
        <td>Pipelined processor from the digital electronics course (see image below)</td>
        <td>83 cycles</td>
        <td>3.5 cycles/num</td>
    </tr>
</table>

<p></p>

<table><tr><td>
    <img style="max-width:50rem" src="{{ url_for('static', filename='tomasoldos/course.png') }}"></img>
    <i>The old aquarium themed pipelined processor I made for the digital electronics course. The red numbers are the 4 16-bit registers.</i>
</td><td>
    <img style="max-width:50rem" src="{{ url_for('static', filename='tomasoldos/fib.png') }}"></img>
    <i>Resulting sequence placed in memory</i>
</td></tr></table>


<!---
## Specific implementations

I may have gone into too much detail in this chunk of the article, but if you are interested in the specific implementations of any of the blocks they can be found below.

### Single Reservation Station

<table>
    <tr><td>
        <img src="{{ url_for('static', filename='tomasoldos/singlestationblock.png') }}"></img>
        <i>SingleRS graphical block</i>
    </td>
    <td>
        <img src="{{ url_for('static', filename='tomasoldos/singlestation.png') }}"></img>
        <i>Inputs, busy, ready, and op outputs.</i>
    </td>
    </tr><tr>
    <td colspan="2">
        <img src="{{ url_for('static', filename='tomasoldos/singlestationjk.png') }}"></img>
        <i>Vj, Vk, Qj, and Qk of the reservation station.</i>
    </tr></td>
</table>

Each reservation station stores an instruction that is either waiting to be executed or is currently begin executed. It takes in the `openRSIns` values which are issued by the overall issue logic to place instructions inside of reservation stations, and checks if this is the reservation station being opened. It also takes in data from the common data bus (CDB through `res` and `rDone`) which allows it to determine when to clear itself and when to fulfill its dependenceis.

*Optimization*: Since store instructions do not need to be written back to the common data bus as they do not generate any resulting value, the completion of these instructions can just directly clear the reservation station holding the instruction through the `forceClear` input instead of occupying the common data bus.

The `Vj`/`Vk` values are the two operands the instruction will operate on. When opening a station with no dependencies, the `VjNew`/`VkNew` values will be bubbled down through the two muxes and both the `Qj`/`Qk` values will be set to zero to indicate neither of the parameters depend on other reservation stations. Otherwise, the values `QjNew` and/or `QkNew` will be written into the `Qj`/`Qk` values to indicate that one or both of the parameters still depends on another reservation station. These are constantly checked against the completing reservation station coming down the CDB so `Vj`/`Vk` can be updated when their data is ready.

The reservation station is deemed `ready` to be executed when it is busy (contains an instruction) and both `Qj` and `Qk` are 0 (neither parameters depend on a prior uncompleted instruction).

### Reservation Stations

<table>
    <tr><td>
        <img style="max-height:40rem;" src="{{ url_for('static', filename='tomasoldos/stationsblock.png') }}"></img>
        <i>ReservationStations graphical block</i>
    </td>
    <td>
        <img style="max-height:40rem;" src="{{ url_for('static', filename='tomasoldos/stationsinput.png') }}"></img>
        <i>Inputs to the ReservationStations block</i>
    </tr></td>
</table>

The reservation stations block provides one output for each execute unit (ALU, Memory Controller, or Branch Manager), indicating when it is ready to be ran and the instruction/values it is to run with. As with most things in this project, the `ins` outputs contain multiple values as is indicated near the bottom of the block diagram in order to make the final routing cleaner. It takes in the (up to) two reservation stations and values the issue logic is telling it to open. These are forwarded directly to the individual reservation stations, as seen in the above section, which are responsible for determining wheter they should be opened. 

The results from the CDB come in from the top, and the optimization described above with bypassing the CDB for store results can be seen in the `store bypass` inputs on the right.

In order for the issue logic to know which reservation stations are clear and can have instructions stored in them, the `Vacant RS#` outputs each give two clear reservation stations ready to store an incoming instruction.

<table>
    <tr><td>
        <img src="{{ url_for('static', filename='tomasoldos/stationsalu.png') }}"></img>
        <i>The 3 ALU reservation stations</i>
    </td>
    <td>
        <img src="{{ url_for('static', filename='tomasoldos/stationsjmp.png') }}"></img>
        <i>The single jump reservation station</i>
    </td>
    </tr><tr>
    <td colspan="2">
        <img src="{{ url_for('static', filename='tomasoldos/stationsldst.png') }}"></img>
        <i>The 3 load/store reservation stations and logic to ensure they run in order</i>
    </tr></td>
</table>

The stations are split up depending on which execution units they are to interface with. There are 3 ALU reservation stations (indicies 1-3) each interface with one ALU; The 3 load/store reservation stations (indicies 4-6) interface with one memory controller running the most recent memory access; One final reservation station is for the branch manager (index 7) determining when the processor should jump.

To the right of the ALU stations, you can see two vertical lines of muxes, which are used to determine which reservation stations are clear so the issue logic knows which ones it can write new instructions to. To the right of the load/store stations, you will see these same two lines of muxes, with an additional one determining which reservation station is to be run next, to ensure all memory accesses run in order. The logic the left of the laod/store stations tracks which station is next to be written to and which is next to be ran, again to help ensure memory accesses are run in order.

The jump station is pretty basic, interfacing directly with the CDB and `openIns`s just as the other stations do. The purpose of having this station is that since the processor depends on the result of the instruction right before a jmpn to determine whether or not it should jump (jmpn = jump if last is negative), you must be able to track a dependancy on said instruction, which is done through the `Qj` value.

### Execution Units / Common Data Bus

<table>
    <tr><td>
        <img src="{{ url_for('static', filename='tomasoldos/executionunits.png') }}"></img>
        <i>Execution Units</i>
    </td>
    <td>
        <img src="{{ url_for('static', filename='tomasoldos/cdb.png') }}"></img>
        <i>Common Data Bus implementation</i>
    </tr></td>
</table>

The execution units themselves are relativly simple given the limited ISA:

- ALU units - take in two operands and either add them, subtract them, or, for `ldi` and `mv` instructions, simply output the first operand which was stored in `Vj`. Since these all take less than a cycle to execute, the `done?` output can be set on immediatly, but it should be noted that the processor would be able to handle multi-cycle ALU instructions.
- Memory controller - take in either a load or a store instruction, set the `addr`, `ram in`, and `WE` pins of the memory block accordingly, and write back to the CDB or the store bypass once done.
- Branch - just check if `conditional negative value` is negative and write the address to be jumped to onto the common data bus if the processor should jump. This is then handled by the `Program Counter` logic, which monitors the common data bus.

The common data bus selects two finishing reservation stations per cycle to be written back to the rest of the processor. Given more than two instruction finishing on a single clock cycle, the common data bus favors writing back branches over loads/stores and loads/stores over ALU instructions. Since reservation stations only clear when their index is written back to the common data bus, any excess finishing execution units (>2 at once) will remain occupied untill their results are written back to the common data bus.

### Registers / Register Stats

<table>
    <tr>
        <td colspan="2">
            <img src="{{ url_for('static', filename='tomasoldos/statsblock.png') }}"></img>
            <i>RegisterBank and RegisterStats graphical blocks</i>
        </td>
    </tr><tr>
        <td>
            <img src="{{ url_for('static', filename='tomasoldos/statsinput.png') }}"></img>
            <i>RegisterStats inputs</i>
        </td>
        <td>
            <img src="{{ url_for('static', filename='tomasoldos/statsoutput.png') }}"></img>
            <i>RegisterStats outputs</i>
        </td>
    </tr>
    <tr>
        <td>
            <img src="{{ url_for('static', filename='tomasoldos/statssingle.png') }}"></img>
            <i>RegisterStats single register stat tracker (rest are identical just with a different constant number on the left)</i>
        </td>
        <td>
            <img src="{{ url_for('static', filename='tomasoldos/statsrecent.png') }}"></img>
            <i>RegisterStats recent instruction result tracker</i>
        </td>
    </tr>
</table>

TODO:
- Registers/register stats
- Issue logic
- PC/Fetch
--->
