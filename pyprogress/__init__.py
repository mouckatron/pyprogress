#! /usr/bin/python2.7

import datetime
import itertools
import sys
import threading
import time


class ProgressBar(object):
    """Show a progress bar and update it everytime increment is called"""
    def __init__(self, total, width=40, name="", showcounter=True, progresschar="#", timecount=False, completionprediction=False, colored=False):
        """
        :param int total: The total count of items being worked on
        :param int width: The width of the progress bar to output, default 40
        :param boolean showcounter: Show the completed/total counter
        :param str progresschar: The character to use in the progress bar, default '#'
        :param boolean timecount: Show the time counter
        :param boolean completionprediction: Show the completion prediction time counter
        :param boolean colored: Color the Items per Second if increased or decreased
        """
        self._total = total
        self._width = float(width)
        self._name = name
        self._progresschar = progresschar
        self._ips_colored = colored

        self._progress = 0
        self._pstr = ""
        self._lenpstr = 0
        self._maxpstr = 0

        self._ended = False
        self._timecount = timecount
        self._runtime = None
        self._completionprediction = completionprediction
        self._cp_timeavg = None
        self._ips_previous = 0

        self._pstr_fmt = "%s%s[{pc:%s}]%s%s" % ("{timecount} " if timecount else "",
                                                "{completionprediction} " if completionprediction else "",
                                                width,
                                                " {p}/{t}" if showcounter else "",
                                                " {ips}/s" if not isinstance(self, DoubleProgressBar) else "")

    def __del__(self):
        self.end()

    def _predict_completion(self):
        try:
            # return "{} {} {} {} {}".format(self._runtime.seconds, self._progress, (float(self._runtime.seconds) / float(self._progress)), self._total, (self._total - self._progress))
            # ( current runtime / current progress ) * ( total items - current progress )
            return "{:.3f}".format(((float(self._runtime.seconds) / float(self._progress)) * (self._total - self._progress)))
        except ZeroDivisionError:
            return None

    def _item_per_sec(self):
        try:
            _value = float(self._progress) / self._runtime.seconds
        except ZeroDivisionError:
            return None
        else:
            if self._ips_colored:
                if _value >= self._ips_previous:
                    s = "\033[92m{:.3f}\033[0m".format(_value)
                else:
                    s = "\033[91m{:.3f}\033[0m".format(_value)
                self._ips_previous = _value
            else:
                s = "{:.3f}".format(_value)
        return s

    def begin(self):
        if self._timecount or self._completionprediction:
            self._timecount = datetime.datetime.utcnow()
        sys.stdout.write(self._name + " ")
        self._write()

    def end(self):
        if not self._ended:
            try:
                self.write()
                sys.stdout.write("\n")
                sys.stdout.flush()
            except AttributeError:
                # sys is already gone
                pass
        self._ended = True

    def update(self, progress):
        self._progress = progress
        self._write()

    def inc(self):
        self._progress += 1
        self._write()

    def _write(self):
        self.write()

    def write(self):

        sys.stdout.write("\b"*self._maxpstr)
        if self._timecount is not False:
            self._runtime = (datetime.datetime.utcnow() - self._timecount)
        try:
            pc = self._progresschar * int(((self._width/self._total)*self._progress))
        except ZeroDivisionError:
            pc = ""
        self._pstr = self._pstr_fmt.format(**{
            "timecount": (str(self._runtime) if self._timecount else ''),
            "completionprediction": (str(self._predict_completion()) if self._completionprediction else ''),
            "pc": pc,
            "p": self._progress,
            "t": self._total,
            "ips": self._item_per_sec()
        })
        self._lenpstr = len(self._pstr) if self._ips_colored is False else len(self._pstr)-9
        if self._lenpstr > self._maxpstr:
            self._maxpstr = self._lenpstr
        sys.stdout.write(self._pstr)
        sys.stdout.write(" " * (self._maxpstr - self._lenpstr))  # add spaces to the max length the string ever was to clear any extra characters
        sys.stdout.flush()


class ThreadedProgressBar(ProgressBar, threading.Thread):

    def __init__(self, total, width=40, name="", showcounter=True, progresschar="#", timecount=False, completionprediction=False, colored=False):
        """
        :param int total: The total count of items being worked on
        :param int width: The width of the progress bar to output, default 40
        :param str name: The name of the data set being worked on to know what the progress bar is for
        :param boolean showcounter: Show the completed/total counter
        :param str progresschar: The character to use in the progress bar, default '#'
        :param boolean timecount: Show the time counter
        :param boolean completionprediction: Show the completion prediction time counter
        """
        super(ThreadedProgressBar, self).__init__(total, width, name, showcounter, progresschar, timecount, completionprediction, colored=colored)

        self._finished = False
        threading.Thread.__init__(self)
        self.daemon = True

    def run(self):
        self.begin()
        while not self._finished:
            self.write()
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                self._finished = True

        self.end()

    def finish(self):
        self._finished = True

    def _write(self):
        # overriding this method with nothing means write will not get called on updates
        pass


class DoubleProgressBar(ProgressBar):

    def __init__(self, total, total2, width=40, name="", showcounter=True, progresschar="#", totalcount=False, timecount=False, completionprediction=False, colored=False):
        """
        :param int total: The total count of items being worked on
        :param int total2: The total count of the subtask items being worked on
        :param int width: The width of the progress bar to output, default 40. Sub bar is half width of the main bar
        :param str name: The name of the data set being worked on to know what the progress bar is for
        :param boolean showcounter: Show the completed/total counter
        :param str progresschar: The character to use in the progress bar, default '#'
        :param boolean totalcount: Total number of items worked on
        :param boolean timecount: Show the time counter
        :param boolean completionprediction: Show the completion prediction time counter
        """

        super(DoubleProgressBar, self).__init__(total,
                                                width=width,
                                                name=name,
                                                showcounter=showcounter,
                                                progresschar=progresschar,
                                                timecount=timecount,
                                                completionprediction=completionprediction,
                                                colored=colored)

        self._total2 = total2

        self._progress2 = 0
        self._pstr2 = ""

        self.totalcount = totalcount
        self._totalcount = 0
        if completionprediction:
            self._cp_timeavg2 = None
            if total2 is not None:
                self._cp_sizecnt2 = 1
                self._cp_sizeavg2 = total2
            else:
                self._cp_sizecnt2 = 0
                self._cp_sizeavg2 = 0

        self._pstr2_fmt = " [{pc:%s}]%s%s {ips}/s" % (
                                                          int((width/2.0)),
                                                          " {p}/{t}" if showcounter else "",
                                                          "  total:{tc}" if totalcount else "")

    def _predict_completion(self):
        try:
            # ( current runtime / current progress ) * ( total items - current progress )
            #
            # current progress = ( (big progress -1) * agv small total ) + small progress
            # current total = ( big total * avg small total )
            # ( current runtime / ( (big progress-1) * avg small total ) + small progress )   *
            # ( (big total * avg small total ) - ( ( big total - 1 ) * avg small total )
            current_progress = float(((self._progress-1) * self._cp_sizeavg2) + self._progress2)
            return "{:.3f}".format(((float(self._runtime.seconds) / current_progress) *
                                    ((self._total * self._cp_sizeavg2) - current_progress)))
        except ZeroDivisionError:
            return None

    def _item_per_sec(self):
        try:
            _value = float(self._totalcount) / self._runtime.seconds
        except ZeroDivisionError:
            return None
        else:
            if self._ips_colored:
                if _value > self._ips_previous:
                    return "\033[92m{:.3f}\033[0m".format(_value)
                else:
                    return "\033[91m{:.3f}\033[0m".format(_value)
                self._ips_previous = _value
            else:
                return "{:.3f}".format(_value)

    def total2(self, total):
        self._total2 = total
        self._cp_sizecnt2 += 1
        self._cp_sizeavg2 += ((total - self._cp_sizeavg2) / self._cp_sizecnt2)

    def update2(self, progress):
        self._totalcount += (progress - self._progress2)
        self._progress2 = progress
        self._write()

    def inc2(self):
        self._totalcount += 1
        self._progress2 += 1
        self._write()

    def reset2(self):
        self._progress2 = 0
        self._write()

    def _write(self):
        self.write()

    def write(self):
        sys.stdout.write("\b"*self._maxpstr)
        if self._timecount is not False:
            self._runtime = (datetime.datetime.utcnow() - self._timecount)
        self._pstr = self._pstr_fmt.format(**{
            "timecount": (str(self._runtime) if self._timecount else ''),
            "completionprediction": (str(self._predict_completion()) if self._completionprediction else ''),
            "pc": self._progresschar * int(((self._width/self._total)*self._progress)),
            "p": self._progress,
            "t": self._total
        })
        fmt2 = {
            "p": self._progress2,
            "t": self._total2,
            "tc": self._totalcount if self.totalcount is not None else '',
            "ips": self._item_per_sec()
        }
        try:
            fmt2['pc'] = self._progresschar * int((((self._width/2.0)/self._total2)*self._progress2))
        except ZeroDivisionError:
            fmt2['pc'] = ''
        self._pstr2 = self._pstr2_fmt.format(**fmt2)
        self._lenpstr = len(self._pstr+self._pstr2) if self._ips_colored is False else len(self._pstr+self._pstr2)-9
        if self._lenpstr > self._maxpstr:
            self._maxpstr = self._lenpstr
        sys.stdout.write(self._pstr+self._pstr2)
        sys.stdout.write(" " * (self._maxpstr - self._lenpstr))  # add spaces to the max length the string ever was to clear any extra characters
        sys.stdout.flush()


class ThreadedDoubleProgressBar(DoubleProgressBar, threading.Thread):

    def __init__(self, total, total2, width=40, name="", showcounter=True, progresschar="#", totalcount=False, timecount=False, completionprediction=False, colored=False):
        """
        :param int total: The total count of items being worked on
        :param int total2: The total count of the subtask items being worked on
        :param int width: The width of the progress bar to output, default 40. Sub bar is half width of the main bar
        :param str name: The name of the data set being worked on to know what the progress bar is for
        :param boolean showcounter: Show the completed/total counter
        :param str progresschar: The character to use in the progress bar, default '#'
        :param boolean totalcount: Total number of items worked on
        :param boolean timecount: Show the time counter
        :param boolean completionprediction: Show the completion prediction time counter
        """
        super(ThreadedDoubleProgressBar, self).__init__(total,
                                                        total2,
                                                        width=width,
                                                        name=name,
                                                        showcounter=showcounter,
                                                        progresschar=progresschar,
                                                        totalcount=totalcount,
                                                        timecount=timecount,
                                                        completionprediction=completionprediction,
                                                        colored=colored)

        self._finished = False
        threading.Thread.__init__(self)
        self.daemon = True

    def run(self):
        self.begin()
        while not self._finished:
            self.write()
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                self._finished = True

        self.end()

    def finish(self):
        self._finished = True

    def _write(self):
        # overriding this method with nothing means write will not get called on updates
        pass


class Spinner(threading.Thread):

    def __init__(self):
        """Simple waiting spinner, no options"""
        threading.Thread.__init__(self)
        self.daemon = True
        self._finished = False
        self._spinner = itertools.cycle(['-', '/', '|', '\\'])

    def run(self):
        sys.stdout.write(self._spinner.next())
        while not self._finished:
            sys.stdout.write("\b{}".format(self._spinner.next()))  # write the next character
            sys.stdout.flush()                # flush stdout buffer (actual character display)
            time.sleep(0.5)

        sys.stdout.write("\n")
        sys.stdout.flush()

    def stop(self):
        self._finished = True


class Counter(threading.Thread):

    def __init__(self, total=None, initial=0):
        """Simple progress counter

        :param total: The total items being worked on if available
        :type total: int or None
        :param int initial: The initial value of the counter, default 0
        """
        threading.Thread.__init__(self)
        self.daemon = True
        self._finished = False
        self.counter = initial
        self.total = total
        self.write = self._write1 if total is not None else self._write2
        self._strlen = 0

    def inc(self, value=1):
        self.counter += value

    def _write1(self):
        """ write with total """
        s = "{}/{}".format(self.counter, self.total)
        sys.stdout.write("\b"*self._strlen)
        sys.stdout.write(s)
        sys.stdout.flush()
        self._strlen = len(s)

    def _write2(self):
        """ write without total"""
        sys.stdout.write("\b"*self._strlen)
        sys.stdout.write(str(self.counter))
        sys.stdout.flush()
        self._strlen = len(str(self.counter))

    def run(self):
        while not self._finished:
            self.write()
            time.sleep(1)
        self.write()

    def stop(self):
        self._finished = True


if __name__ == '__main__':
    import random
    import signal

    def sigint_handler(signal, frame):
        try:
            tpb
        except NameError:
            pass
        else:
            tpb.finish()
            tpb.join()
            del tpb
        try:
            tdpb
        except NameError:
            pass
        else:
            tdpb.finish()
            tdpb.join()
            del tdpb
        try:
            s
        except NameError:
            pass
        else:
            s.stop()
            s.join()
            del s
        try:
            c
        except NameError:
            pass
        else:
            c.stop()
            c.join()
            del c
        sys.exit()
    signal.signal(signal.SIGINT, sigint_handler)

    # SINGLE PROGRESS BAR
    if len(sys.argv) == 1 or '--pb' in sys.argv:
        firstsize = 10
        pb = ProgressBar(firstsize, name="ProgressBar", timecount=False, completionprediction=True, colored=True)
        pb.begin()

        for x in range(firstsize):
            pb.inc()
            time.sleep(random.random()*2)
        pb.end()

    # DOUBLE PROGRESS BAR
    if len(sys.argv) == 1 or '--dpb' in sys.argv:
        firstsize = 10
        secondsize = random.randint(5, 15)
        pb = DoubleProgressBar(firstsize, secondsize, name="DoubleProgressBar", totalcount=True, timecount=True, completionprediction=True, colored=True)
        pb.begin()

        for x in range(firstsize):
            pb.inc()
            pb.reset2()
            pb.total2(secondsize)
            for y in range(secondsize):
                pb.inc2()
                time.sleep(random.random())
            secondsize = random.randint(5, 15)
        pb.end()

    # THREADED PROGRESS BAR
    if len(sys.argv) == 1 or '--tpb' in sys.argv:
        firstsize = 10
        tpb = ThreadedProgressBar(firstsize, name="ThreadedProgressBar", timecount=True, completionprediction=True, colored=True)
        tpb.start()

        for x in range(firstsize):
            tpb.inc()
            time.sleep(random.random()*2)

        tpb.finish()
        tpb.join()
        del tpb

    # THREADED DOUBLE PROGRESS BAR
    if len(sys.argv) == 1 or '--tdpb' in sys.argv:
        firstsize = 5
        secondsize = random.randint(3, 5)
        tdpb = ThreadedDoubleProgressBar(firstsize, secondsize, name="ThreadedDoubleProgressBar", totalcount=True, timecount=True, completionprediction=True, colored=True)
        tdpb.start()

        for x in range(firstsize):
            tdpb.inc()
            tdpb.reset2()
            tdpb.total2(secondsize)
            for y in range(secondsize):
                tdpb.inc2()
                time.sleep(random.random())
            secondsize = random.randint(3, 5)
        tdpb.finish()
        tdpb.join()
        del tdpb

    # SPINNER
    if len(sys.argv) == 1 or '--sp' in sys.argv:
        sys.stdout.write("\nSpinner ")

        s = Spinner()
        s.start()
        time.sleep(5)
        s.stop()
        s.join()

    # COUNTER
    if len(sys.argv) == 1 or '--cnt' in sys.argv:
        sys.stdout.write("\nCounter ")

        c = Counter(total=20)
        c.start()
        for x in range(20):
            c.inc()
            time.sleep(random.random())
        c.stop()
        c.join()