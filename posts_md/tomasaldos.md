Tomasulo's algorithm
Post
5-24-2026
Tomasulo's algorithm is a clever algorithm used in computer processor design which can dynamically schedule instructions, allowing for multiple instructions to be run at a time and allowing them to be run out of their program order once they no longer depend on any prior unfinished instructions. Originally developed in 1967, the algorithm was created to address the issue of multi-cycle floating-point instructions stalling processors. It served as a way to allow processors to continue operating during these long operations and established the principles which nearly all modern out-of-order processors rely on. In this article I'll explain the basics of the algorithm and there will be a follow up article with my own implementation of it in Logisim.

If you want a deeper understanding of the algorithm and instruction-level parallelism (ILP) as a whole, I would strongly recommend checking out Chapter 3 of _Computer Architecture: A Quantitative Approach_, this is where I learned most of the stuff in this post. I should note that Tomasulo's algorithm was removed in the 7th edition in favor of other register renaming methods, but you can still find the 6th edition on [internet archive](https://dn790008.ca.archive.org/0/items/computerarchitectureaquantitativeapproach6thedition/Computer%20Architecture%3A%20A%20Quantitative%20Approach%206th%20Edition.pdf) (p. 201 or pdf page 233 for Tomasulo's).

## The Algorithm

Tomasulo's algorithm is a method of dynamic scheduling, which allows for multiple instructions to be queued and ran when they no longer depend on any prior instructions that have not yet completed. The instructions do not need to be executed in the order they came in, allowing for instructions that are ready to be executed to not be held up by previous instructions which may take a long time to execute. This is useful as often times instructions which take a long time to execute will stall a simple processor (ex. memory fetches or some floating point operations), while there are instructions after said instruction would be able to run without that instruction having finished. Tomasulo's algorithm allows these instructions which do not depend on any prior uncompleted instructions to begin running, even when there are instructions before them that have not completed.

The algorithm largely revolves around **Reservation Stations**, which track dependencies between instructions and are able to determine when an instruction is ready to be ran. Each time an instruction is loaded from memory, it is stored in a reservation station until it has been completed and the reservation station can be cleared. Each reservation station stores the following:

- Busy flag - indicates whether this station is holding an instruction.
- Op - The instruction to be ran (ex. add, ldi, etc.)
- Vj, Vk - The values to be operated on once the instruction is ready to be executed (ex. the values of `rs1` and `rs2` in RISC-V).
- Qj, Qk - The indexes of the reservation stations storing the instructions which `Vj` and `Vk` depend on, or a 0 if they are valid and do not depend on any other prior uncompleted instruction. Once the instructions in the reservation stations this instruction depends on are completed, these are set to 0 to indicate they no longer depend on any prior uncompleted instruction (ex. the unfinished instruction `rs1` depends on may have the index of the reservation station storing the instruction stored in `Qj` to indicate `Vj` is waiting on another instruction).

Once both `Qj` and `Qk` of a reservation station are set to zero indicating the instruction has no prior dependencies, the processor can begin execute of the instruction using `Op`, `Vj`, and `Vk`.

The rest of the algorithm along with a more in depth example of the use of reservation stations will be introduced via an example of the algorithm being used to run the following program:

    # R0 and R1 are registers
    # Starting state: R0=0, R1=2
    ldi R0,1    # load immediate, R0 = 1
    add R1,R0   # add,            R1 = R1 + R0

*Step 1*: The first ldi instruction is loaded into a reservation station resulting in the following state:

**Reservation Stations**

<table>
    <tr>
        <td><b>Reservation Station Index</b></td>
        <td><b>Busy</b></td>
        <td><b>Op</b></td>
        <td><b>Vj</b></td>
        <td><b>Vk</b></td>
        <td><b>Qj</b></td>
        <td><b>Qk</b></td>
    </tr>
    <tr>
        <td>1</td>
        <td>1</td>
        <td>ldi</td>
        <td>1</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
    </tr>
    <tr>
        <td>2</td>
        <td>0</td>
        <td>none</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
    </tr>
</table>

In the first available reservation station, `#1`,  The value to be operated on (1) is stored in `Vj`, and `Vk` remains unused since there is no second operand for ldi. Since the instruction did not depend on any prior instructions, both `Qj` and `Qk` are 0.

*Step 2*: Assuming the first instruction has not yet been ran (for example's sake), the second instruction will load into the reservation stations resulting in the following state:

__Reservation Stations__

<table>
    <tr>
        <td><b>Reservation Station Index</b></td>
        <td><b>Busy</b></td>
        <td><b>Op</b></td>
        <td><b>Vj</b></td>
        <td><b>Vk</b></td>
        <td><b>Qj</b></td>
        <td><b>Qk</b></td>
    </tr>
    <tr>
        <td>1</td>
        <td>1</td>
        <td>ldi</td>
        <td>1</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
    </tr>
    <tr>
        <td>2</td>
        <td>1</td>
        <td>add</td>
        <td>2</td>
        <td>0</td>
        <td>0</td>
        <td>1</td>
    </tr>
</table>

The first operand (R1) did not depend on any prior instructions, so its value (2) is loaded into `Vj` and a 0 is loaded into `Qj`. The second operand (R0) depends on the prior ldi instruction, so a 0 is temporarily loaded into `Vk` and a 1 is loaded into `Qk` indicating that this value depends on the instruction in the 1st reservation station.

Since both `Qj` and `Qk` in the first reservation station are 0, the processor knows that it does not depend on any prior uncompleted instructions and is ready to be ran. Once the instruction finishes, the result, along with the reservation station index it came from, are written onto a **Common Data Bus**. Once a reservation station sees its index on the common data bus, it knows the instruction it holds has finished and it can be cleared. This also allows for any reservation stations which has a matching `Qj`/`Qk` index to the finishing instruction to update.

Back to the example, once the first ldi instruction finishes, its result is written back onto the common data bus, which the second reservation station will see and use to clear its dependency on the first. 

*Step 3*: The state after the first instruction finishes will be:

__Reservation Stations__

<table>
    <tr>
        <td><b>Reservation Station Index</b></td>
        <td><b>Busy</b></td>
        <td><b>Op</b></td>
        <td><b>Vj</b></td>
        <td><b>Vk</b></td>
        <td><b>Qj</b></td>
        <td><b>Qk</b></td>
    </tr>
    <tr>
        <td>1</td>
        <td>0</td>
        <td>none</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
    </tr>
    <tr>
        <td>2</td>
        <td>1</td>
        <td>add</td>
        <td>2</td>
        <td>1</td>
        <td>0</td>
        <td>0</td>
    </tr>
</table>

Since the add instruction finished, the first reservation station can be cleared. The second reservation station is able to match its value `Qk` to the finishing reservation station, and store the value from the common data bus (1) into `Vj`.

In this last state, the processor can see that both `Qj` and `Qk` of reservation station 2 are 0, so the add instruction no longer depends on any prior instructions and is able to be ran.

The last part of the algorithm is how the processor is able to tell when an instruction depends on a prior uncompleted instruction. In our example, this would be how we determine that the add instruction depends on R0, which had yet been written to by the prior ldi instruction. This is done with a separate **Register Status** tracker, which stores the index of the reservation station each register depends on in a value called `Qi` (i.e. there is one `Qi` value per register). Like the `Qj` and `Qk` values, this stores a 0 if the register does not depend on any reservation stations.

If we go back through our example tracking the register status file, we can see how the dependency of addi on ldi can be inferred.

```
Starting state: R0=0, R1=2
ldi R0,1
add R1,R0
```

*Step 1*: The add instruction is loaded into the first reservation station and a dependency of R0 on this station is noted.

__Reservation Stations__

<table>
    <tr>
        <td><b>Reservation Station Index</b></td>
        <td><b>Busy</b></td>
        <td><b>Op</b></td>
        <td><b>Vj</b></td>
        <td><b>Vk</b></td>
        <td><b>Qj</b></td>
        <td><b>Qk</b></td>
    </tr>
    <tr>
        <td>1</td>
        <td>1</td>
        <td>ldi</td>
        <td>1</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
    </tr>
    <tr>
        <td>2</td>
        <td>0</td>
        <td>none</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
    </tr>
</table>

__Register Status File__

<table>
    <tr>
        <td><b>Register</b></td>
        <td>R0</td>
        <td>R1</td>
        <td>R2</td>
        <td>R3</td>
    </tr>
    <tr>
        <td><b>Qi</b></td>
        <td>1</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
    </tr>
    <tr>
        <td><b>Value</b></td>
        <td>0</td>
        <td>2</td>
        <td>0</td>
        <td>0</td>
    </tr>
</table>

Now, when any instruction is loaded that depends on R0, it will be able to recognize that this register depends on the unfinished first reservation station, and set its corresponding `Q` value to the first reservation station.

*Step 2*: The add instruction is loaded into the second reservation station.

__Reservation Stations__

<table>
    <tr>
        <td><b>Reservation Station Index</b></td>
        <td><b>Busy</b></td>
        <td><b>Op</b></td>
        <td><b>Vj</b></td>
        <td><b>Vk</b></td>
        <td><b>Qj</b></td>
        <td><b>Qk</b></td>
    </tr>
    <tr>
        <td>1</td>
        <td>1</td>
        <td>ldi</td>
        <td>1</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
    </tr>
    <tr>
        <td>2</td>
        <td>1</td>
        <td>add</td>
        <td>2</td>
        <td>0</td>
        <td>0</td>
        <td>1</td>
    </tr>
</table>

__Register Status File__

<table>
    <tr>
        <td><b>Register</b></td>
        <td>R0</td>
        <td>R1</td>
        <td>R2</td>
        <td>R3</td>
    </tr>
    <tr>
        <td><b>Qi</b></td>
        <td>1</td>
        <td>2</td>
        <td>0</td>
        <td>0</td>
    </tr>
    <tr>
        <td><b>Value</b></td>
        <td>0</td>
        <td>2</td>
        <td>0</td>
        <td>0</td>
    </tr>
</table>

Along with marking its dependency on the first reservation station, loading add instruction also marks R1 as depending on the second reservation station so any following instructions could mark their dependency on the add instruction if needed.

*Step 3*: The ldi instruction finishes execution and is written back to the common data bus.

__Reservation Stations__

<table>
    <tr>
        <td><b>Reservation Station Index</b></td>
        <td><b>Busy</b></td>
        <td><b>Op</b></td>
        <td><b>Vj</b></td>
        <td><b>Vk</b></td>
        <td><b>Qj</b></td>
        <td><b>Qk</b></td>
    </tr>
    <tr>
        <td>1</td>
        <td>0</td>
        <td>none</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
    </tr>
    <tr>
        <td>2</td>
        <td>1</td>
        <td>add</td>
        <td>2</td>
        <td>1</td>
        <td>0</td>
        <td>0</td>
    </tr>
</table>

__Register Status File__
<table>
    <tr>
        <td><b>Register</b></td>
        <td>R0</td>
        <td>R1</td>
        <td>R2</td>
        <td>R3</td>
    </tr>
    <tr>
        <td><b>Qi</b></td>
        <td>0</td>
        <td>2</td>
        <td>0</td>
        <td>0</td>
    </tr>
    <tr>
        <td><b>Value</b></td>
        <td>1</td>
        <td>2</td>
        <td>0</td>
        <td>0</td>
    </tr>
</table>

Since the result of the first reservation station has been written back to the common data bus, the register status file can now clear its dependency (`Qi`) of R0 on this station.

It should be noted that if later instructions also write to R1 before the add instruction has been ran, their reservation station index will override the `Qi` value for R1 as any further instructions would be depending on that new reservation station. Values are only written into the registers themselves if the finishing reservation station is equal to the `Qi` of that register.

One thing that was not discussed in this example is how loads and stores are managed. Since these can not be run out of order (two writes to the same address must be executed in the order they came in as), they are instead stored in separate load/store buffers that ensure they are executed in order. These are nearly identical to the reservation stations in terms of tracking dependencies, but must be ran in the order that the instructions came in.

A longer example of the algorithm can be found on page 201 of `Computer Archetecture: A Quantitative Approch, 6th edition` ([here](https://dn790008.ca.archive.org/0/items/computerarchitectureaquantitativeapproach6thedition/Computer%20Architecture%3A%20A%20Quantitative%20Approach%206th%20Edition.pdf) on internet archive, pdf page 233).

I hope this article served as a good intro to Tomasulo's algorithm and was also a bit enjoyable! If you'd like to see my implementation of the algorithm, check out my follow up post once I finish writing it! As always, thanks for reading ^_^.
