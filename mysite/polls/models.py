import datetime
import textwrap

import PIL
from PIL import Image, ImageDraw, ImageFont
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Image(models.Model):
    path = models.CharField(max_length=200)

    def __str__(self):
        return self.path


class Mem(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    upper_text = models.CharField(max_length=200)
    lower_text = models.CharField(max_length=200)

    @staticmethod
    def generate_meme(image_path,
                      dst_path,
                      top_text,
                      bottom_text='',
                      font_path='',
                      font_size=9,
                      stroke_width=5):
        # load image
        im = PIL.Image.open(image_path)

        draw = ImageDraw.Draw(im)
        image_width, image_height = im.size

        # load font
        font = ImageFont.truetype(font=font_path, size=int(image_height * font_size) // 100)

        # convert text to uppercase
        top_text = top_text.upper()
        bottom_text = bottom_text.upper()

        # text wrapping
        char_width, char_height = font.getsize('A')
        chars_per_line = image_width // char_width
        top_lines = textwrap.wrap(top_text, width=chars_per_line)
        bottom_lines = textwrap.wrap(bottom_text, width=chars_per_line)

        # draw top lines
        y = 10
        for line in top_lines:
            line_width, line_height = font.getsize(line)
            x = (image_width - line_width) / 2
            draw.text((x, y), line, fill='white', font=font, stroke_width=stroke_width, stroke_fill='black')
            y += line_height

        # draw bottom lines
        y = image_height - char_height * len(bottom_lines) - 15
        for line in bottom_lines:
            line_width, line_height = font.getsize(line)
            x = (image_width - line_width) / 2
            draw.text((x, y), line, fill='white', font=font, stroke_width=stroke_width, stroke_fill='black')
            y += line_height

        # save meme
        im.save(dst_path)

    def __str__(self):
        return self.image
