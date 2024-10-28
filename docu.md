# CAN-Tester Equipment Documentation

This equipment is designed to:
- Simulate CAN/CAN FD messages on the BUS.
- Monitor the BUS

The objective of this documentation is to provide a clear understanding of the following:
1. Message output Porcess
2. Labeling Definitions
3. Basic Configurations
4. General Capabilities

## Set-Up
1. After power up, you ll be able to access the equipment interface. 
The interface should look like this.

![CAN](https://github.com/user-attachments/assets/8941e56d-daf7-447e-b1c5-d7b9ea174dcd)


The CAN Shield uses two CAN Controllers, CAN0 and CAN1.
One of them will be Sender and the other one Receiver.
Why is that? We canot set the same controller to send and read the bus at the same time.
For example, CAN0 will be the sender, this module will output the messages on the bus.
CAN1 will be the receiver, the main objective of this module is to monitor the bus.

2. **CAN MODULES**
- Set CAN RECEIVER - CAN0 and CAN SENDER - CAN1 

3. **Baudrate**

The ID Baudrate is the data speed of the message (ID + PAYLOAD)
The DATA BADURATE is used if you want Flexible Data-Rate. 
```diff
- Only if FD and BRS checkboxes are selected, the ID and the PAYLOAD will be sent at different speed.
```
Example:
You set ID BAUDRATE = 1M and DATA BAUDRATE = 5M.
If you send a message, the whole message will be sent at 1M.
Instead, if you check the FD and the BRS checkboxes, the ID will be sent at 1M and the payload at 5M. 

4. **Sample Point (Optional)**
DATA SP specifies the location inside each bit period where the CAN controller looks at the state of the bus and determines if it is a logic zero (dominant) or logic one (recessive).
You can enter values between 0 and 1. Example: 0.5, 0.75

6. **Status**
Set Status UP. This will enable the CAN modules with the given specifications.

7. **(RTR, BRS, EXT, FD) Checkboxes**

- RTR - Remote Request Frames = Send empty package rquesting data from the identifier.
ExAMPLE. ID = 0x123, PAYLOAD = NULL 

- BRS - Bit Rate Switch = Increases speed after the arbitration field is transmitted.
Basically, ID and PAYLOAD are sent are different speed.

- EXT - Extended ID = Specifies that the ID is extended. 
Example: ID = 0x12345678, 0XAABBCCDD

- FD - Flexible Data = Specifies that a message with different speed is going to be sent.

7. **Message Structure Format**
- CAN CLASSIC ID/CAN FD ID examples: 0x123, 0xFFF, 0xAAA.
- CAN CLASSIC PAYLOAD/CAN FD PAYLOAD examples: CAFE, 12345678, AABBCCDD

- CAN EXT ID examples: 0x12345678, 0xAABBCCDD

8. **ADD TO QUEUE**

This will add the message from your entryboxes to the Message List Queue.

*Note. The message is not sent yet.*

You can add more than one message to the queue.
After entering all the messages, press SEND QUE to send the messages.

9. **Extra functions (Import, Save, Clear, Edit, Loop)**
- Import = Used to insert a log with CAN Messages on the queue. Needs to be a text file.
- Save = Used to save the current log on the queue.
- Clear = Clears the whole queue list.
- Edit = Used to change the message composition.
Select the message you want to edit and press edit. The message is now on the entryboxes area and can be changed.
- Loop = Checkbox used to resend the whole queue after one sec.

```diff
- Note: You can only import an already saved list using the save function of the interface. Also, specify the extension on the name at saving. Ex. mylog.txt
```

10. **Info list and Random Loop**
- The info list will output interface info like CAN Messages format errors or CAN Modules state (UP/DOWN)

- Random Loop, used to generate traffic on the bus(CAN Classic or CAN FD). Select the delay between messages, the number of messg and START. 


Have Fun!
