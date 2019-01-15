#!/usr/bin/python3
'Pychat!'
import readline
import os
import colorama
import leancloud as AV
import yaml
import time
import _user
import _args
import _room

VERSION = 1.5
CONFIGDIR = os.path.expandvars('$HOME') + '/.config/pychat/'
ARGS = _args.init()
Chat = AV.Object.extend('talk')
Notice = AV.Object.extend('notice')
config = yaml.load(open(CONFIGDIR + 'init.yaml'))
if ARGS.debug:
    AV.init('ULc6VQsRiQr4NENpfoJpfd52-gzGzoHsz', 'iYA2I9QBd6SJ1fwGOQxceyQD')
else:
    AV.init("IDDU0rkX0FJ9hi2SFQgP1YIt-gzGzoHsz", "K3zSqgPWAssTN9kyKWDJWG8y")
colorama.init()

def welcome(): # {{{1
    'welcome screen'
    print(colorama.Fore.BLUE, end='')
    print('┌─────────────────────────┐')
    print('│        Welcome !!!      │')
    print('│                         │')
    print('│  p   y   c   h   a   t  │')
    print('│                         │')
    print('│     VERSION:  ', VERSION, '     │')
    print('└─────────────────────────┘')
    if ARGS.debug:
        info = Notice.create_without_data('5c3025e667f35600631c87d0')
    else:
        info = Notice.create_without_data('5c29d4ab9f5454007005488b')
    info.fetch()
    print(colorama.Fore.RED, 'Notice:\n', info.get('content'))
    print(colorama.Style.RESET_ALL)

def command(comms): # {{{1
    'deal with a command'
    res, prinfo = 'null', ''
    comms = comms.split(' ')
    if comms == []:
        return res, prinfo
    com = comms[0]
    if com in ('quit', 'q'):
        res, prinfo = 'quit', 'You quited!'
    elif com in ('w', 'who'):
        res, prinfo = 'who', 'The people who\' re in this room:'
    elif com in ('p', 'printall'):
        res = 'printall'
    elif com in ('k', 'killroot'):
        res = 'killroot'
    elif com in ('h', 'help'):
        prinfo = 'This is help message:\n \
                use q[uit] to quit\n \
                use h[elp] to get help\n \
                use w[ho] to see who\'re online\n \
                use g[et] to get new message (refresh)\n \
                use e[dit] to edit configuration file\n \
                use k[illroot] to print all messages without root\'s\n \
                use p[rint] to print all messages\n \
                All command should begin with \':\''
    elif com in ('e', 'edit'):
        os.system('edit ~/.config/pychat/init.yaml')
        global config
        config = yaml.load(open(CONFIGDIR + 'init.yaml'))
        prinfo = 'edited'
    elif com in ('c', 'call'):
        pass
    elif com in ('g', 'get'):
        pass # Do nothing
    else:
        prinfo = 'No such a command!'
    return res, prinfo

def main(): # {{{1
    'Main function'
    user = AV.User()
    welcome()
    if _user.init(user, ARGS, config) == 1:
        print('failed')
        return 1
    comres, cominfo = '', ''
    if ARGS.debug:
        room = _room.ChatRoom(user, \
                Chat.create_without_data('5c30264bfb4ffe005fd22a11'))
    else:
        room = _room.ChatRoom(user, \
                Chat.create_without_data('5c29b63afb4ffe005fb0de88'))
    fetch = True
    root_com = None
    try:
        import _root
        root_com = _root.Command(AV, ARGS.debug)
    except ModuleNotFoundError:
        pass
    while comres != 'quit':
        lasttime = time.time()
        if comres == 'printall':
            room.printall(fetch=fetch)
        elif comres == 'killroot':
            room.printall(printroot=False, fetch=fetch)
        else:
            room.printnew(fetch=fetch)
        if cominfo != '':
            print(cominfo)
        if comres == 'who':
            print(room.user_list())
        if config.get('line') in ('', None):
            con = input('Input yours(input :h to get help)$ ')
        else:
            con = input(config.get('line'))
        print(colorama.Cursor.UP(1), end='')
        print('                                                                                ')
        print(colorama.Cursor.UP(1), end='')
        if not room.exist(): # room.todo fetch there
            print()
            print('Sorry, you must leave now')
            break
        comres, cominfo = 'null', ''
        if con == '':
            if config.get('banempty'):
                cominfo = 'input EMPTY!'
            fetch = False
        elif con[0] == ':':
            comres, cominfo = command(con[1:])
            fetch = False
        elif con[0] == '!':
            os.system(con[1:])
            print()
            fetch = False
        elif con[0] == '@':
            if root_com:
                root_com.command(con[1:])
            else:
                import _messagebox
                _messagebox.warning('You cannot use root command!')
            fetch = True
        else:
            room.send(con)
            fetch = False
        if time.time() < lasttime + 1.5:
            print('Wait a moment, you type so fast!')
            time.sleep(lasttime + 1.5 - time.time())

def toexit(res): # {{{1
    'to exit the execute and return [res]'
    exit(res)

if __name__ == '__main__': # {{{1
    try:
        # os.system('cd ~/.config/pychat/upstream/; git pull; make;')
        toexit(main())
    except EOFError as err:
        print(colorama.Fore.RED)
        print('Unexcept EOF!', colorama.Style.RESET_ALL)
        toexit(1)
    except KeyboardInterrupt as err:
        print(colorama.Fore.RED)
        print('Unexcept Ctrl-C!', colorama.Style.RESET_ALL)
        toexit(1)

# }}}1
