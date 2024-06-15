### for install please run this command:
```bash
cd && git clone https://github.com/BEQSONA-cmd/Debug_Leaks.git && cd Debug_Leaks && ./install.sh
```


### After that you have to open NEW terminal and run:
```bash
dl "Program Name" (with/without arguments)
```
example
```c
dl ./push_swap 4 2 3 1
```
or if you have endless program you have to add flag '-e'

(program that needs to press or click something to finish the process)
```c
dl -e ./philo 5 400 100 100
```
and you can stop the process with just clicking (Ctrl + c)

### !!! and dont forget to add '-g' flag in Makefile !!!
```c
CFLAGS = -Wall -Wextra -Werror -g
```

#### 'dl' stand for (debug leaks) :)

## Here is guide for how you can fix leaks with this tool:
<img src="https://github.com/BEQSONA-cmd/Debug_Leaks/blob/main/gif/Debug_leaks_Guide.gif" width="600">
