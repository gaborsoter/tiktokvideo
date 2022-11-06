import re

import numpy as np

from moviepy.tools import cvsecs
from moviepy.video.VideoClip import TextClip, VideoClip
from customTextClip import CustomTextClip

class CustomSubtitlesClip(VideoClip):
    def __init__(self, subtitles, make_textclip=None):
        
        VideoClip.__init__(self, has_constant_size=False)

        if isinstance(subtitles, str):
            subtitles = file_to_subtitles(subtitles)

        #subtitles = [(map(cvsecs, tt),txt) for tt, txt in subtitles]
        self.subtitles = subtitles
        self.textclips = dict()

        if make_textclip is None:
            make_textclip = lambda txt: CustomTextClip(txt, font='Georgia-Bold',
                                        fontsize=24, color='white',
                                        stroke_color='black', stroke_width=2)

        self.make_textclip = make_textclip
        self.start=0
        self.duration = max([tb for ((ta,tb), txt) in self.subtitles])
        self.end=self.duration
        
        def add_textclip_if_none(t):
            """ Will generate a textclip if it hasn't been generated asked
            to generate it yet. If there is no subtitle to show at t, return
            false. """
            sub =[((ta,tb),txt) for ((ta,tb),txt) in self.textclips.keys()
                   if (ta<=t<tb)]
            if not sub:
                sub = [((ta,tb),txt) for ((ta,tb),txt) in self.subtitles if
                       (ta<=t<tb)]
                if not sub:
                    return False
            sub = sub[0]
            if sub not in self.textclips.keys():
                self.textclips[sub] = self.make_textclip(sub[1])

            return sub

        def make_frame(t):
            sub = add_textclip_if_none(t)
            return (self.textclips[sub].get_frame(t) if sub
                    else np.array([[[0,0,0]]]))

        def make_mask_frame(t):
            sub = add_textclip_if_none(t)
            return (self.textclips[sub].mask.get_frame(t) if sub
                    else np.array([[0]]))
        
        self.make_frame = make_frame
        hasmask = bool(self.make_textclip('T').mask)
        self.mask = VideoClip(make_mask_frame, ismask=True) if hasmask else None

    def in_subclip(self, t_start= None, t_end= None):

        def is_in_subclip(t1,t2):
            try:
                return (t_start<=t1<t_end) or (t_start< t2 <=t_end)
            except:
                return False
        def try_cropping(t1,t2):
            try:
                return (max(t1, t_start), min(t2, t_end))
            except:
                return (t1, t2)
        return [(try_cropping(t1,t2), txt) for ((t1,t2), txt) in self.subtitles
                                               if is_in_subclip(t1,t2)]

    


    def __iter__(self):
        return iter(self.subtitles)
    


    def __getitem__(self, k):
        return self.subtitles[k]

    

    def __str__(self):

        def to_srt(sub_element):
            (ta, tb), txt = sub_element
            fta = cvsecs(ta)
            ftb = cvsecs(tb)
            return "%s - %s\n%s"%(fta, ftb, txt)
        
        return "\n\n".join(to_srt(s) for s in self.subtitles)
    


    def match_expr(self, expr):

        return SubtitlesClip([e for e in self.subtitles
                              if re.findall(expr, e[1]) != []])
    

    def write_srt(self, filename):
        with open(filename, 'w+') as f:
            f.write(str(self))



def file_to_subtitles(filename):
    times_texts = []
    current_times = None
    current_text = ""
    with open(filename,'r') as f:
        for line in f:
            times = re.findall("([0-9]*:[0-9]*:[0-9]*,[0-9]*)", line)
            if times:
                current_times = [cvsecs(t) for t in times]
            elif line.strip() == '':
                times_texts.append((current_times, current_text.strip('\n')))
                current_times, current_text = None, ""
            elif current_times:
                current_text += line
    return times_texts