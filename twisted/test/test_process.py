from __future__ import division, absolute_import



from io import BytesIO

from twisted.python.compat import _PY3, networkString, xrange
from twisted.python.filepath import FilePath, _asFilesystemBytes
# Get the current Python executable as a bytestring.
pyExe = FilePath(sys.executable)._asBytesPath()
        bytesToSend = b"bytes"
        p.childDataReceived(1, bytesToSend)
        self.assertEqual(received, [bytesToSend])
        bytesToSend = b"bytes"
        p.childDataReceived(2, bytesToSend)
        self.assertEqual(received, [bytesToSend])
        self.data = b''
        self.err = b''
        self.transport.write(b"abcd")
            if self.data != b"abcd":
            self.transport.write(b"1234")
            if self.err != b"1234":
            self.transport.write(b"abcd")
    s = b"1234567" * 1001
        if self.buffer[self.count:self.count+len(data)] != data:
    @classmethod
            self, pyExe, [pyExe, b"-c", self.program] + argv, env=env)
    program = networkString(
        return b''.join(chunks).split(b'\0')
    program = networkString(
        "items = environ.items()\n"
        environString = b''.join(chunks)
        environ = iter(environString.split(b'\0'))
                k = next(environ)
                v = next(environ)
        scriptPath = FilePath(__file__).sibling(b"process_twisted.py").path
        env = {b"PYTHONPATH": _asFilesystemBytes(os.pathsep.join(sys.path))}
        reactor.spawnProcess(p, pyExe, [pyExe, b"-u", scriptPath], env=env,
        p.transport.write(b"hello, world")
        p.transport.write(b"abc")
        p.transport.write(b"123")
            self.assertEqual(p.outF.getvalue(), b"hello, worldabc123",
        scriptPath = FilePath(__file__).sibling(b"process_echoer.py").path
        procTrans = reactor.spawnProcess(p, pyExe,
                                    [pyExe, scriptPath], env=None)
        scriptPath = FilePath(__file__).sibling(b"process_tester.py").path
        reactor.spawnProcess(p, pyExe, [pyExe, b"-u", scriptPath], env=None)
        scriptPath = FilePath(__file__).sibling(b"process_tester.py").path
        args = [pyExe, b"-u", scriptPath]
            reactor.spawnProcess(p, pyExe, args, env=None)
        scriptPath = FilePath(__file__).sibling(b"process_echoer.py").path
        reactor.spawnProcess(p, pyExe, [pyExe, scriptPath], env=None)
            self.assertEqual(len(p.buffer), len(p.s * p.n))
        args = [br'a\"b ', br'a\b ', br' a\\"b', br' a\\b', br'"foo bar" "',
                b'\tab', b'"\\', b'a"b', b"a'b"]
        scriptPath = FilePath(__file__).sibling(b"process_cmdline.py").path
        reactor.spawnProcess(p, pyExe, [pyExe, b"-u", scriptPath] + args,
                             env=None, path=None)
            self.assertEqual(p.errF.getvalue(), b"")
            {b"foo": 2},
            {b"foo": b"egg\0a"},
            {3: b"bar"},
            {b"bar\0foo": b"bar"}]
            [pyExe, 2],
            b"spam",
            [pyExe, b"foo\0bar"]]
            badArgs.append([pyExe, badUnicode])
                reactor.spawnProcess, p, pyExe, [pyExe, b"-c", b""], env=env)
                reactor.spawnProcess, p, pyExe, args, env=None)
    encodedValue = b"UNICODE"
            self.assertEqual(argv, [b'-c', self.encodedValue])
        scriptPath = FilePath(__file__).sibling(b"process_reader.py").path
                                     pyExe, [pyExe, b"-u", scriptPath], env=None,
        if self.verbose: print("closing stdin [%d]" % num)
        if self.verbose: print(self.pp[0].finished, self.pp[1].finished)
        if self.verbose: print("starting processes")
        if self.verbose: print("kill [%d] with SIGTERM" % num)
        if self.verbose: print(self.pp[0].finished, self.pp[1].finished)
        if self.verbose: print("starting processes")
        if self.verbose: print("starting processes")
        if self.verbose: print("starting processes")
    data = b""
        self.transport.writeToChild(0, b"abcd")
                if self.data != b"righto":
                self.data = b""
                self.transport.writeToChild(3, b"efgh")
                if self.data != b"closed":
        scriptPath = FilePath(__file__).sibling(b"process_fds.py").path
        reactor.spawnProcess(p, pyExe, [pyExe, b"-u", scriptPath], env=None,
        scriptPath = FilePath(__file__).sibling(b"process_linger.py").path
        reactor.spawnProcess(p, pyExe, [pyExe, b"-u", scriptPath], env=None,
                             b"here is some text\ngoodbye\n")
        self.outF = BytesIO()
        self.errF = BytesIO()
class PosixProcessBase(object):
        binLoc = FilePath('/bin').child(commandName)
        usrbinLoc = FilePath('/usr/bin').child(commandName)

        if binLoc.exists():
            return binLoc._asBytesPath()
        elif usrbinLoc.exists():
            return usrbinLoc._asBytesPath()

        reactor.spawnProcess(p, cmd, [b'true'], env=None,
        reactor.spawnProcess(p, pyExe,
                             [pyExe, b'-c', b'import sys; sys.exit(1)'],
        scriptPath = FilePath(__file__).sibling(b"process_signal.py").path
        reactor.spawnProcess(p, pyExe, [pyExe, b"-u", scriptPath], env=None,
            reactor.spawnProcess(p, cmd, [b'false'], env=None,
                errData = b"".join(p.errData + p.outData)
                self.assertIn(b"Upon execvpe", errData)
                self.assertIn(b"Ouch", errData)
        scriptPath = FilePath(__file__).sibling(b"process_echoer.py").path
            ErrorInProcessEnded(), pyExe,
            [pyExe, scriptPath],
    @type fdio: C{BytesIO} or C{BytesIO}
    readData = b""
        Fake C{os.fdopen}. Return a file-like object whose content can
        be tested later via C{self.fdio}.
        if flag == "wb":
            self.fdio = BytesIO()
        else:
            assert False
    def getfilesystemencoding(self):
        """
        Return a fixed filesystem encoding.

        @return: A fixed value of "utf8".
        """
        return "utf8"


        cmd = b'/mock/ouch'
            reactor.spawnProcess(p, cmd, [b'ouch'], env=None,
        cmd = b'/mock/ouch'
        reactor.spawnProcess(p, cmd, [b'ouch'], env=None,
        cmd = b'/mock/ouch'
        self.assertRaises(SystemError, reactor.spawnProcess, p, cmd, [b'ouch'],
        cmd = b'/mock/ouch'
            reactor.spawnProcess(p, cmd, [b'ouch'], env=None,
            self.assertIn(b"RuntimeError: Bar", self.mockos.fdio.getvalue())
        cmd = b'/mock/ouch'
            reactor.spawnProcess(p, cmd, [b'ouch'], env=None,
        cmd = b'/mock/ouch'
        reactor.spawnProcess(p, cmd, [b'ouch'], env=None,
        cmd = b'/mock/ouch'
            reactor.spawnProcess(p, cmd, [b'ouch'], env=None,
        cmd = b'/mock/ouch'
            reactor.spawnProcess(p, cmd, [b'ouch'], env=None,
        cmd = b'/mock/ouch'
        proc = reactor.spawnProcess(p, cmd, [b'ouch'], env=None,
        cmd = b'/mock/ouch'
        proc = reactor.spawnProcess(p, cmd, [b'ouch'], env=None,
        cmd = b'/mock/ouch'
        proc = reactor.spawnProcess(p, cmd, [b'ouch'], env=None, usePTY=False)
        cmd = b'/mock/ouch'
        proc = reactor.spawnProcess(p, cmd, [b'ouch'], env=None, usePTY=False)
        cmd = b'/mock/ouch'
        proc = reactor.spawnProcess(p, cmd, [b'ouch'], env=None, usePTY=False)
        cmd = b'/mock/ouch'
        proc = reactor.spawnProcess(p, cmd, [b'ouch'], env=None, usePTY=False)
        reactor.spawnProcess(p, pyExe,
                             [pyExe, b"-c",
                              networkString("import sys; sys.stderr.write"
                                            "('{0}')".format(value))],
            self.assertEqual(b"42", p.errF.getvalue())
        s = b"there's no place like home!\n" * 3
        reactor.spawnProcess(p, cmd, [cmd, b"-c"], env=None, path="/tmp",
        scriptPath = FilePath(__file__).sibling(b"process_tty.py").path
        reactor.spawnProcess(p, pyExe, [pyExe, b"-u", scriptPath], env=None,
        p.transport.write(b"hello world!\n")
                b"hello world!\r\nhello world!\r\n",
        pyArgs = [pyExe, b"-u", b"-c", b"print('hello')"]
            usePTY=1, childFDs={1:b'r'})
                ValueError("Wrong exit code: %s" % (v.exitCode,)))
        scriptPath = FilePath(__file__).sibling(b"process_stdinreader.py").path
        reactor.spawnProcess(p, pyExe, [pyExe, b"-u", scriptPath], env=None,
        p.transport.write(b"hello, world")
        pyArgs = [pyExe, b"-u", b"-c", b"print('hello')"]
                          reactor.spawnProcess, p, pyExe, pyArgs, uid=1)
                          reactor.spawnProcess, p, pyExe, pyArgs, gid=1)
                          reactor.spawnProcess, p, pyExe, pyArgs, usePTY=1)
                          reactor.spawnProcess, p, pyExe, pyArgs, childFDs={1:'r'})
        scriptPath = FilePath(__file__).sibling(b"process_signal.py").path
        reactor.spawnProcess(p, pyExe, [pyExe, b"-u", scriptPath], env=None)
        pyArgs = [pyExe, b"-u", b"-c", b"print('hello')"]
        comspec = bytes(os.environ["COMSPEC"])
        cmd = [comspec, b"/c", pyExe, scriptPath]
        for name, mode in [(j(self.foobaz, "executable"), 0o700),
                           (j(self.foo, "executable"), 0o700),
                           (j(self.bazfoo, "executable"), 0o700),
                           (j(self.bazfoo, "executable.bin"), 0o700),
            f = open(name, "wb")
    output = b''
    errput = b''
            p, pyExe, [
                pyExe, b'-u', b'-c',
                networkString('try: input = raw_input\n'
                'except NameError: pass\n'
                'input()\n'
                '    os.write(%d, b"foo\\n")\n'
                'sys.exit(42)\n' % (fd,))
        p.transport.write(b'go\n')
        self.assertEqual(p.output, b'')
            if _PY3:
                self.assertIn(b'BrokenPipeError', errput)
            else:
                self.assertIn(b'OSError', errput)
                self.assertIn(b'Broken pipe', errput)
            self.assertEqual(errput, b'')