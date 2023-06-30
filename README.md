FLOW:

1. **First the arduino ide takes a reading from all the sensors and uploads the telemetry data into a binary file.**

2. **The binary file format is stored in a yaml document that adheres to the kataistruct format.**

3. **Next the binary file is parsed to read the header and other fields.**

4. **(The original code is written in python using the kataistruct library but the arduino ide doesnt support this and so, if the code has to be written in c, it will be using a basic parser.) (so ive written two documents to exhibit this)**

5. **Last, the document is decoded and displayed (python)**
