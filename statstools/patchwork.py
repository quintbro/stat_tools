from PIL import Image
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
    
    
    def _build(self, build_formula):
        formula = re.sub(r"\s*", "", string=build_formula)
        p_list = re.split(r"[\(\)]", formula)
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
            
    def quilt(self, build_formula):
        new_plot = self._build(build_formula)
        self.new_plot = new_plot
        return self.plots[new_plot]