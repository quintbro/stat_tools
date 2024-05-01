from PIL import Image, ImageDraw, ImageFont
import io
from IPython.display import display
import regex as re
import plotnine

class PGrid:
    def __init__(self, plot_dict):
        self.plots = plot_dict
    
    def _add_plots(self, plots_list):
        imgs = []
        for plot in plots_list:
            if isinstance(self.plots[plot], Image.Image):
                img = self.plots[plot]
            else: 
                fig = self.plots[plot].draw()
                buf = io.BytesIO()
                fig.savefig(buf, format='png')
                buf.seek(0)
                img = Image.open(buf)
            imgs.append(img)

        combined_image = imgs[0]
        for i in range(1, len(imgs)):
            new_image = Image.new('RGB', (combined_image.width + imgs[i].width, 
                                               max(combined_image.height, imgs[i].height)), color="white")
            if combined_image.height > imgs[i].height:
                h1 = round(imgs[i].height / 2)
                h2 = round(combined_image.height / 2)
                new_image.paste(combined_image, (0, 0))
                new_image.paste(imgs[i], (combined_image.width, h2 - h1))
                combined_image = new_image
            else:
                h1 = round(combined_image.height / 2)
                h2 = round(imgs[i].height / 2)
                new_image.paste(combined_image, (0, h2 - h1))
                new_image.paste(imgs[i], (combined_image.width, 0))
                combined_image = new_image
        new_plot_name = "~".join(plots_list)
        self.plots[new_plot_name] = combined_image
        return new_plot_name


    def _divide_plots(self, plots_list):
        imgs = []
        for plot in plots_list:
            if isinstance(self.plots[plot], Image.Image):
                img = self.plots[plot]
            else:
                fig = self.plots[plot].draw()
                buf = io.BytesIO()
                fig.savefig(buf, format='png')
                buf.seek(0)
                img = Image.open(buf)
            imgs.append(img)

        combined_image = imgs[0]
        for i in range(1, len(imgs)):
            new_image = Image.new('RGB', (max(combined_image.width, imgs[i].width), 
                                               combined_image.height + imgs[i].height), color="white")
            if combined_image.width > imgs[i].width:
                h1 = round(imgs[i].width / 2)
                h2 = round(combined_image.width / 2)
                new_image.paste(combined_image, (0, 0))
                new_image.paste(imgs[i], (h2 - h1, combined_image.height))
                combined_image = new_image
            else:
                h1 = round(combined_image.width / 2)
                h2 = round(imgs[i].width / 2)
                new_image.paste(combined_image, (h2 - h1, 0))
                new_image.paste(imgs[i], (0, combined_image.height))
                combined_image = new_image
        
        new_plot_name = "%".join(plots_list)
        self.plots[new_plot_name] = combined_image
        return new_plot_name
    
    def _parse_string(self, string):
        depth = 0
        parts = []
        current_part = ""
        itr = 0
        for char in string:
            itr += 1
            depth1 = depth
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
            if (depth1 == 0 and depth == 1) or itr == len(string) or (depth1 == 1 and depth == 0):
                if itr == len(string) and char != ")" and char != "(":
                    current_part += char
                if current_part.strip():
                    parts.append(current_part)
                    current_part = ""
            else:
                current_part += char
        return parts
    
    
    def _build(self, build_formula):
        formula = re.sub(r"\s*", "", string=build_formula)
        # p_list = re.split(r"[\(\)]", formula)
        p_list = self._parse_string(formula)
        form_list = [i for i in p_list if i != ""]
        if len(form_list) == 1:
            plots_to_add = re.split(r"\+", form_list[0])
            plots_to_add = [i for i in plots_to_add if i != ""]
            if len(plots_to_add) > 1:
                new_plot_name =  self._add_plots(plots_to_add)
                return new_plot_name

            plots_to_divide = re.split(r"/", form_list[0])
            plots_to_divide = [i for i in plots_to_divide if i != ""]
            if len(plots_to_divide) > 1:
                return self._divide_plots(plots_to_divide)
            else:
                return form_list[0]

        self.form_list = form_list
        return self._build("".join([self._build(thing) for thing in form_list]))
            
    def quilt(self, build_formula, size = "auto", title = None, title_size = 40):
        '''
        Parameters
        ----------
        build_formula : string
            A combination of plot names "+", "/", and "()" that determine the plot grid
        size : tuple
            A tuple detailing the size of the resulting image, each dimension will be the max
            size and the image will retain it's aspect ratio
        title : string
            A string for a title to be put on the entire plot
        title_size : int
            the size of the title
        '''
        new_plot = self._build(build_formula)
        self.grid_img = self.plots[new_plot]
        self.no_title = self.plots[new_plot]
        if title is not None:
            self.grid_img = self.title(title, title_size)
        if size != "auto":
            self.grid_img.thumbnail(size)
        return self.grid_img
    
    def title(self, title, size = 40):
        ''' Adds a title to a quilted plotgrid object, a better way to do this is to 
        specify the title as an arguement of the quilt method.
        Parameters
        ----------
        title : string
            Title to be added
        size : int
            Size of the title to be added

        Returns
        -------
        PIL image object containing the plot with the added title
        '''
        title_img = Image.new('RGB', (self.no_title.width, size + 20), color="white")
        draw = ImageDraw.Draw(title_img)
        font = ImageFont.truetype("arial.ttf", size)
        text_bbox = draw.textbbox((0,0),title, font = font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        x_coord = (title_img.width - text_width) // 2
        y_coord = (title_img.height - text_height) // 2

        draw.text((x_coord, y_coord), title, "black", font, align="center")
        new_image = Image.new('RGB', (title_img.width, self.no_title.height + title_img.height))
        new_image.paste(title_img, (0, 0))
        new_image.paste(self.no_title, (0, title_img.height))
        return new_image