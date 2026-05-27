import io
import flet as ft
from PIL import Image,ImageFilter,ImageDraw,ImageFont
import base64
import time
class Redactor(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.image = None
        self.dopping_image = None
        self.help_count1 = 0
        self.current_path = None
        self.dop_path = None
        self.file_picker = ft.FilePicker(on_result=self.pick_result)
        self.file_picker2 = ft.FilePicker(on_result=self.pick_result2)
        self.count = 0
        self.image_width = 0
        self.image_height = 0
        self.last_click_time = 0
        self.double_click_time = 0.3
        self.user_text1 = ft.TextField(color='orange',width = 180,height=60,label_style=ft.TextStyle(color='orange'),label='Start X')
        self.user_text2 = ft.TextField(color='orange',width = 180,height=60 ,label_style=ft.TextStyle(color='orange'),label='End X')
        self.user_text3 = ft.TextField(color='orange',width = 180,height=60 ,label_style=ft.TextStyle(color='orange'),label='Start Y')
        self.user_text4 = ft.TextField(color='orange',width = 180,height=60 ,label_style=ft.TextStyle(color='orange'),label='End Y')
        self.resize_width = ft.TextField(color='orange',width = 100,height=35,label_style = ft.TextStyle(color='orange'),label='Width')
        self.resize_height = ft.TextField(color='orange', width=100,height=35,label_style=ft.TextStyle(color='orange'),label='Height')
        self.width_main = ft.TextField(width=150,color=ft.colors.ORANGE,label='width',label_style=ft.TextStyle(color='orange'),height=30)
        self.height_main = ft.TextField(width=150,color=ft.colors.ORANGE,label='height',label_style=ft.TextStyle(color='orange'),height=30)
        self.movements = ft.Text('Movements : 0',width=150,color=ft.colors.RED,height=30)
        self.radius = ft.TextField(width=180,height=60,label_style=ft.TextStyle(color=ft.colors.ORANGE),label='Radius(pixels)',color=ft.colors.ORANGE,disabled=True,value='0')
        self.number_w = None
        self.number_h = None
        self.image_container = ft.Container(width=self.number_w,height=self.number_h)# Container для отображения image
        self.image_dopping_container = ft.Container(width=50,height=50)
        self.btn1 = ft.Radio(value='option 1', label='with',disabled=False)
        self.btn2 = ft.Radio(value='option 2', label='without',disabled=False)
        self.radio = ft.RadioGroup(
            content=ft.Column(
                controls=[
                    self.btn1,
                    self.btn2,
                    #self.discard,
                    #self.btn3
                ]
            ),
            on_change=self.choice_pencil,
            disabled=True
        )
        self.btn1_choice = ft.Radio(value='choice1',label='Paste Image(Upper Left)')
        self.btn2_choice = ft.Radio(value='choice2',label='Mask')
        self.btn3_choice = ft.Radio(value='choice3',label='Paint')

        self.discard = ft.ElevatedButton(width=180, height=60, color='red', text='Discard first point', on_click=self.change_fields,disabled=True)
        self.radio_choice = ft.RadioGroup(content=ft.Column([
            self.btn1_choice,
            self.btn2_choice,
            self.discard,
            self.btn3_choice,

            ]),on_change=self.choice_pencil,disabled=True)
        self.color1 = ft.Radio(value='number1',label='Black')
        self.color2 = ft.Radio(value='number2', label='Red')
        self.color3 = ft.Radio(value='number3', label='Blue')
        self.color4 = ft.Radio(value='number4',label='White')
        self.color5 = ft.Radio(value='number5', label='Green')
        self.color6 = ft.Radio(value='number6',label='Pink')
        self.color7 = ft.Radio(value='number7',label='Violet')
        self.radio_colors = ft.RadioGroup(content=ft.Column([
            ft.Row([
            self.color1,
            self.color2,
            self.color3,
            self.color4,]),
            ft.Row([
            self.color5,
            self.color6,
            self.color7])
        ]),on_change=self.suggestion_color,disabled=True)


        self.gesture1 = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.CLICK,
            on_tap_down=None,
            content=self.image_container)

        self.zoom_count = 0
        self.current_size_main = ft.Text('Size:',color=ft.colors.ORANGE,width = 140)
        self.size_doping = ft.Text('Size:',color=ft.colors.ORANGE,width = 140)

        self.x = 0
        self.y = 0
        self.x_cut = 0
        self.x2_cut = 0
        self.y_cut = 0
        self.y2_cut = 0
        self.count_cut_click = 0
        self.x2 = 0
        self.y2 = 0
        self.x1_dop = 0
        self.x2_dop = 0
        self.count_cl = 0
        self.chet_90 = 0
        self.x_circle = 0
        self.y_circle = 0
        self.list_pictures = []
        self.count_pictures = 0
        self.fixing = -1
        self.overall = 0
        self.color = None
        self.BLACK = (0,0,0,255)
        self.RED = (255,0,0,255)
        self.BLUE = (0,0,255,255)
        self.WHITE = (255,255,255,255)
        self.GREEN = (0,255,0,255)
        self.PINK = (255,192,203,255)
        self.VIOLET = (238,130,238,255)
        self.list_width = []
        self.list_height = []

    def rotate_img_90(self,event):
        if self.current_path:
            if self.zoom_count == 0:
                pillow_image = Image.open(self.current_path)
                self.chet_90 += 1
                if self.chet_90 % 2 != 0:
                     self.image_container.width = self.number_h
                     self.image_container.height = self.number_w
                else:
                    self.image_container.width = self.number_w
                    self.image_container.height =  self.number_h
                changing_image1 = pillow_image.rotate(90,expand = True)
                img_byte = io.BytesIO() #изображение будет хранится в виде байтов
                changing_image1.save(img_byte, format="PNG") #в данном случае изображение не будет сохраняться
                img_byte = img_byte.getvalue()#извлекаем байты
                encoded_img = base64.b64encode(img_byte).decode("ascii") #декод преобразует байтовую строку в текстовую
                self.image_container.content = ft.Image(src_base64=encoded_img, fit=ft.ImageFit.CONTAIN)#обязательно base64
                self.current_path = io.BytesIO(img_byte)
                self.list_pictures.append(self.current_path)
                self.list_width.append(self.image_container.width)
                self.list_height.append(self.image_container.height)
                self.movements.value = f'Movements : {len(self.list_width) - 1}'
                self.overall += 1
                self.fixing = self.overall
            else:
                self.page.show_snack_bar(ft.SnackBar(ft.Text("Please , exit zoom", color='orange'), bgcolor=ft.colors.BLUE_100))
        if self.count == 0:
            self.page.show_snack_bar(ft.SnackBar(ft.Text("You didn't choose a picture",color='orange'),bgcolor=ft.colors.BLUE_100))
        self.image_container.update()
        self.update()
        self.page.update()
    def rotate_img_180(self,event):
        if self.current_path:
            if self.zoom_count == 0:
                pillow_image = Image.open(self.current_path)
                if self.chet_90 % 2 != 0:
                    self.image_container.width = self.number_h
                    self.image_container.height = self.number_w
                elif self.chet_90 % 2 == 0 or self.chet_90 == 0:
                    self.image_container.width = self.number_w
                    self.image_container.height = self.number_h
                changing_image2 = pillow_image.rotate(180,expand=True)
                img_byte = io.BytesIO()
                changing_image2.save(img_byte, format="PNG")
                img_byte = img_byte.getvalue()
                encoded_img = base64.b64encode(img_byte).decode("ascii")
                self.image_container.content = ft.Image(src_base64=encoded_img,fit=ft.ImageFit.CONTAIN)#контаин нжно для того чтобы изображение плавно отображалось
                self.current_path = io.BytesIO(img_byte)
                self.list_pictures.append(self.current_path)
                self.list_width.append(self.image_container.width)
                self.list_height.append(self.image_container.height)
                self.movements.value = f'Movements : {len(self.list_width) - 1}'
                self.overall += 1

            else:
                self.page.show_snack_bar(
                    ft.SnackBar(ft.Text("Please , exit zoom", color='orange'), bgcolor=ft.colors.BLUE_100))
        else:
            self.page.show_snack_bar(ft.SnackBar(ft.Text("You didn't choose a picture",color='orange'),bgcolor=ft.colors.BLUE_100))
        self.update()
        self.page.update()
    def blur(self,event):
        if self.current_path:
             pillow_image = Image.open(self.current_path)
             changing_image4 = pillow_image.filter(ImageFilter.BLUR)
             img_byte = io.BytesIO()
             changing_image4.save(img_byte,format="PNG")
             img_byte = img_byte.getvalue()
             encoded_img = base64.b64encode(img_byte).decode("ascii")
             self.image_container.content = ft.Image(src_base64=encoded_img,fit=ft.ImageFit.CONTAIN)
             self.current_path = io.BytesIO(img_byte)
             self.list_pictures.append(self.current_path)
             self.list_width.append(self.image_container.width)
             self.list_height.append(self.image_container.height)
             self.movements.value = f'Movements : {len(self.list_width) - 1}'
             self.update()
             self.page.update()
        else:
            self.page.show_snack_bar(ft.SnackBar(ft.Text("You didn't choose a picture",color='orange'),bgcolor=ft.colors.BLUE_100))

    def sharpen(self,event):
        if self.current_path:
            pillow_image = Image.open(self.current_path)
            changing_image6 = pillow_image.filter(ImageFilter.SHARPEN)
            img_byte = io.BytesIO()
            changing_image6.save(img_byte, format="PNG")
            img_byte = img_byte.getvalue()
            encoded_img = base64.b64encode(img_byte).decode("ascii")
            self.image_container.content = ft.Image(src_base64=encoded_img,fit=ft.ImageFit.CONTAIN)
            self.current_path = io.BytesIO(img_byte)
            self.list_pictures.append(self.current_path)
            self.list_width.append(self.image_container.width)
            self.list_height.append(self.image_container.height)
            self.movements.value = f'Movements : {len(self.list_width) - 1}'
            self.update()
            self.page.update()
        if self.count == 0:
            self.page.show_snack_bar(ft.SnackBar(ft.Text("You didn't choose a picture",color='orange'),bgcolor=ft.colors.BLUE_100))

    def strongedge(self,event):
        if self.current_path:
            pillow_image = Image.open(self.current_path)
            changing_image8 = pillow_image.filter(ImageFilter.EDGE_ENHANCE_MORE)
            img_byte = io.BytesIO()
            changing_image8.save(img_byte, format="PNG")
            img_byte = img_byte.getvalue()
            encoded_img = base64.b64encode(img_byte).decode("ascii")
            self.image_container.content = ft.Image(src_base64=encoded_img, fit=ft.ImageFit.CONTAIN)
            self.current_path = io.BytesIO(img_byte)
            self.list_pictures.append(self.current_path)
            self.list_width.append(self.image_container.width)
            self.list_height.append(self.image_container.height)
            self.movements.value = f'Movements : {len(self.list_width) - 1}'
            self.update()
            self.page.update()
        if self.count == 0:
            self.page.show_snack_bar(ft.SnackBar(ft.Text("You didn't choose a picture",color='orange'),bgcolor=ft.colors.BLUE_100))

    def silver(self,event):
        if self.current_path:
            pillow_image = Image.open(self.current_path)
            changing_image9 = pillow_image.filter(ImageFilter.EMBOSS)
            img_byte = io.BytesIO()
            changing_image9.save(img_byte, format="PNG")
            img_byte = img_byte.getvalue()#for ft.image
            encoded_img = base64.b64encode(img_byte).decode("ascii")
            self.image_container.content = ft.Image(src_base64=encoded_img, fit=ft.ImageFit.CONTAIN)
            self.current_path = io.BytesIO(img_byte)
            self.list_pictures.append(self.current_path)
            self.list_width.append(self.image_container.width)
            self.list_height.append(self.image_container.height)
            self.movements.value = f'Movements : {len(self.list_width) - 1}'
            self.update()
            self.page.update()
        if self.count == 0:
            self.page.show_snack_bar(ft.SnackBar(ft.Text("You didn't choose a picture",color='orange'),bgcolor=ft.colors.BLUE_100))

    def crop_rectangle(self,event):
        if self.current_path:
            pillow_image = Image.open(self.current_path).convert("RGBA")
            width,height = pillow_image.size
            mask = Image.new('L',(width,height),255)
            draw = ImageDraw.Draw(mask)
            if int(self.user_text1.value) < int(self.user_text2.value) and int(self.user_text3.value) < int(self.user_text4.value):
                 draw.rectangle((int(self.user_text1.value),int(self.user_text3.value),int(self.user_text2.value)+1,int(self.user_text4.value)+1),fill=0)
            else:
                self.page.show_snack_bar(ft.SnackBar(ft.Text('X End must be more then X Start and Y End must be more then Y Start',color='orange'),bgcolor=ft.colors.BLUE_100))
            new_image = Image.new('RGBA',(width,height),(0,0,0,0))
            new_image.paste(pillow_image,(0,0),mask)
            img_byte = io.BytesIO()
            new_image.save(img_byte,format="PNG")
            img_byte = img_byte.getvalue()
            encoded_image = base64.b64encode(img_byte).decode("ascii")
            self.image_container.content = ft.Image(src_base64=encoded_image,fit=ft.ImageFit.CONTAIN)
            self.current_path = io.BytesIO(img_byte)
            self.list_pictures.append(self.current_path)
            self.list_width.append(self.image_container.width)
            self.list_height.append(self.image_container.height)
            self.movements.value = f'Movements : {len(self.list_width) - 1}'
        if (int(self.user_text2.value) == 0 or int(self.user_text4.value)) == 0 and self.count == 1:
            self.page.show_snack_bar(
                ft.SnackBar(ft.Text("X End and Y End must be different from zero", color='orange'), bgcolor=ft.colors.BLUE_100))
        if self.count == 0:
            self.page.show_snack_bar(ft.SnackBar(ft.Text("You didn't choose a picture",color='orange'),bgcolor=ft.colors.BLUE_100))
        self.update()
        self.page.update()

    def choice_pencil(self,event):
        selected_value = self.radio_choice.value
        if self.current_path:
            if selected_value == 'choice1':
                self.gesture1.on_tap_down = self.click_paste
                self.radius.disabled = True
                self.radio_colors.disabled = True
                self.discard.disabled = True
            elif selected_value == 'choice2':
                self.gesture1.on_tap_down = self.clickers
                self.radius.disabled = True
                self.radio_colors.disabled = True
                self.discard.disabled = False
            elif selected_value == 'choice3':
                self.gesture1.on_tap_down = self.painting
                self.radius.disabled = False
                self.radio_colors.disabled = False
                self.discard.disabled = True

        self.gesture1.update()
        self.update()
        self.page.update()

    def zoom_plus(self,event):
        if self.current_path:
            if self.image_container.width > self.image_container.height:
                if self.zoom_count == 0:
                    self.image_container.width *= 1.5
                    self.image_container.height *= 1.5
                    self.zoom_count = 1
                    print(self.list_width)
                else:
                    self.page.show_snack_bar(ft.SnackBar(ft.Text("You've already applied this function",color='orange'),bgcolor=ft.colors.BLUE_100))
            else:
                self.page.show_snack_bar(ft.SnackBar(ft.Text("You can't apply this function because height > width",color='orange'),bgcolor=ft.colors.BLUE_100))
        else:
            self.page.show_snack_bar(ft.SnackBar(ft.Text("You don't have a picture!",color='orange'),bgcolor=ft.colors.BLUE_100))
        self.page.update()
        self.update()
    def zoom_minus(self,event):
        if self.current_path:
            if self.zoom_count == 1:
                self.image_container.width /= 1.5
                self.image_container.height /= 1.5
                self.zoom_count = 0
            else:
                self.page.show_snack_bar(ft.SnackBar(ft.Text("You didn't approximate a picture", color='orange'),bgcolor=ft.colors.BLUE_100))
        else:
            self.page.show_snack_bar(ft.SnackBar(ft.Text("You don't have a picture!",color='orange'),bgcolor=ft.colors.BLUE_100))
        self.page.update()
        self.update()


    def suggestion_color(self,event):
        selected_value = self.radio_colors.value
        if self.current_path:
            if selected_value == 'number1':
                self.color = self.BLACK
            elif selected_value == 'number2':
                self.color = self.RED
            elif selected_value == 'number3':
                self.color = self.BLUE
            elif selected_value == 'number4':
                self.color = self.WHITE
            elif selected_value == 'number5':
                self.color = self.GREEN
            elif selected_value == 'number6':
                self.color = self.PINK
            elif selected_value == 'number7':
                self.color = self.VIOLET
        self.update()
        self.page.update()

    def painting(self,event:ft.TapEvent):
        self.x_circle = int(event.local_x)
        self.y_circle = int(event.local_y)
        if self.current_path:
            img1 = Image.open(self.current_path).convert('RGBA')
            width,height = img1.size
            cont_width = self.image_container.width
            cont_height = self.image_container.height
            print(self.image_container.height)
            kof1 = width/cont_width
            kof2 = height/cont_height
            mask = Image.new('L',(width,height),255)
            draw = ImageDraw.Draw(mask)
            radius = int(self.radius.value)
            if radius == 0:
                self.page.show_snack_bar(ft.SnackBar(ft.Text("Radius can't be zero!",color='orange'),bgcolor=ft.colors.BLUE_100))
            draw.ellipse((self.x_circle*kof1-radius,self.y_circle*kof2-radius,self.x_circle*kof1+radius,self.y_circle*kof2+radius),fill=0) #alpha flood of ellipse
            if self.color:
                new_image = Image.new('RGBA',(width,height),self.color)#color of elipse
                new_image.paste(img1,(0,0),mask)
                img_byte = io.BytesIO()
                new_image.save(img_byte,format='PNG')
                img_byte = img_byte.getvalue()
                encoded_image = base64.b64encode(img_byte).decode('ascii')
                self.image_container.content = ft.Image(src_base64=encoded_image,fit=ft.ImageFit.CONTAIN)
                self.current_path = io.BytesIO(img_byte)
                self.list_pictures.append(self.current_path)
                self.list_width.append(self.image_container.width)
                self.list_height.append(self.image_container.height)
                self.movements.value = f'Movements : {len(self.list_width) - 1}'
            else:
                self.page.show_snack_bar(ft.SnackBar(ft.Text("You didn't choose the color!",color='orange'),bgcolor=ft.colors.BLUE_100))
        else:
            self.page.show_snack_bar(ft.SnackBar(ft.Text("You don't have a main picture!", color='orange'),
                                                     bgcolor=ft.colors.BLUE_100))
        self.update()
        self.page.update()

    def scalable_help(self,event):
        selected_value = self.radio_choice.value
        if self.current_path and selected_value == 'option 1':
            pillow_image = Image.open(self.current_path)
            width , height = pillow_image.size
            new_par1 = width
            new_par2 = height
            draw = ImageDraw.Draw(pillow_image)
            font = ImageFont.load_default(size=40)#random font
            while new_par1 > 0:
                x = new_par1 - 100
                draw.text((x,0),str(x),font=font,fill='orange')
                draw.line((x,0,x,height),width = 3,fill='orange')
                new_par1 -= 100
            while new_par2 > 0:
                y = new_par2 - 100
                draw.text((0,y+10),str(y),font=font,fill='orange')
                draw.line((0,y,width,y),width = 3,fill='orange')
                new_par2 -= 100
            img_byte = io.BytesIO()
            pillow_image.save(img_byte,format="PNG")
            img_byte = img_byte.getvalue()
            encoded_image = base64.b64encode(img_byte).decode("ascii")
            self.image_container.content = ft.Image(src_base64=encoded_image, fit=ft.ImageFit.CONTAIN)
        elif self.current_path and selected_value == 'option 2':
            pillow_image = Image.open(self.current_path)
            img_byte = io.BytesIO()
            pillow_image.save(img_byte , format = "PNG")
            img_byte = img_byte.getvalue()
            encoded_image = base64.b64encode(img_byte).decode("ascii")
            self.image_container.content = ft.Image(src_base64=encoded_image,fit=ft.ImageFit.CONTAIN)
        self.update()
        self.page.update()

    def open(self,event):
        if self.current_path:
            pillow_image = Image.open(self.current_path)
            pillow_image.show()
        if self.count == 0:
            self.page.show_snack_bar(
                ft.SnackBar(ft.Text("You didn't choose a picture", color='orange'), bgcolor=ft.colors.BLUE_100))
            self.update()
            self.page.update()

    def click_paste(self,event:ft.TapEvent):
        self.x1_dop = int(event.local_x)
        self.x2_dop = int(event.local_y)
        if self.count == 1 and self.help_count1 == 1:
            img1 = Image.open(self.current_path)
            width,height = img1.size
            cont_width = self.image_container.width
            cont_height = self.image_container.height
            kof1 = width / cont_width
            kof2 = height / cont_height
            if self.dopping_image:
                img2 = Image.open(self.dop_path)
                img1.paste(img2,(int(self.x1_dop*kof1),int(self.x2_dop*kof2)))
            elif not self.dopping_image:
                self.page.show_snack_bar(ft.SnackBar(ft.Text("You don't have a crucial element!",color='orange'), bgcolor=ft.colors.BLUE_100))
            img_byte = io.BytesIO()
            img1.save(img_byte,format='PNG')
            img_byte = img_byte.getvalue()
            encoded_image = base64.b64encode(img_byte).decode("ascii")
            self.image_container.content = ft.Image(src_base64=encoded_image, fit=ft.ImageFit.CONTAIN)
            self.current_path = io.BytesIO(img_byte)
            self.list_pictures.append(self.current_path)
            self.list_width.append(self.image_container.width)
            self.list_height.append(self.image_container.height)
            self.movements.value = f'Movements : {len(self.list_width) - 1}'
        else:
            self.page.show_snack_bar(ft.SnackBar(ft.Text("You don't have a crucial element!", color='orange'),
                                                     bgcolor=ft.colors.BLUE_100))
        self.update()
        self.page.update()


    def return_image(self,event):
        if len(self.list_pictures) >= 2:
            if self.zoom_count == 0:
                self.current_path = self.list_pictures[-2]
                img1 = Image.open(self.current_path)
                self.list_pictures.pop()
                self.image_container.width = self.list_width[-2]
                self.image_container.height = self.list_height[-2]
                self.list_width.pop()
                self.list_height.pop()
                img_byte = io.BytesIO()
                img1.save(img_byte, format='PNG')
                img_byte = img_byte.getvalue()
                encoded_image = base64.b64encode(img_byte).decode("ascii")
                self.image_container.content = ft.Image(src_base64=encoded_image, fit=ft.ImageFit.CONTAIN)
                self.current_path = io.BytesIO(img_byte)
                self.overall -= 1
                self.fixing -= 1
                self.chet_90 -= 1
                self.movements.value = f'Movements : {len(self.list_width) - 1}'


            else:
                self.page.show_snack_bar(
                    ft.SnackBar(ft.Text("Please , exit zoom", color='orange'), bgcolor=ft.colors.BLUE_100))
        else:
            self.page.show_snack_bar(ft.SnackBar(ft.Text("You returned to the first image",color='orange'),bgcolor=ft.colors.BLUE_100))
        self.image_container.update()
        self.update()
        self.page.update()

    def resize_dop_img(self,event):
        if self.dopping_image:
            new_width = int(self.resize_width.value)
            new_height = int(self.resize_height.value)
            pillow_image = Image.open(self.dopping_image.src)
            changing_image = pillow_image.resize((new_width,new_height),reducing_gap=3.0)#impruve the quality of picture
            w,h = changing_image.size
            img_byte = io.BytesIO()
            changing_image.save(img_byte,format='PNG')
            img_byte = img_byte.getvalue()
            encoded_image = base64.b64encode(img_byte).decode("ascii")
            self.dop_path = io.BytesIO(img_byte)
            self.image_dopping_container.content = ft.Image(src_base64=encoded_image,fit = ft.ImageFit.CONTAIN)
            self.size_doping.value = f'Size: W {w},H {h}'
            self.update()
            self.page.update()

    def resize_main(self,event):
        main_width = int(self.width_main.value)
        main_height = int(self.height_main.value)
        pillow_image = Image.open(self.current_path)
        changing_image = pillow_image.resize((main_width,main_height),reducing_gap=3.0)
        w,h = changing_image.size
        img_byte = io.BytesIO()
        changing_image.save(img_byte,format='PNG')
        img_byte = img_byte.getvalue()
        encoded_image = base64.b64encode(img_byte).decode('ascii')
        self.current_path = io.BytesIO(img_byte)
        self.image_container.content = ft.Image(src_base64 = encoded_image,fit = ft.ImageFit.CONTAIN)
        self.list_pictures.append(self.current_path)
        self.list_width.append(self.image_container.width)
        self.list_height.append(self.image_container.height)
        self.movements.value = f'Movements : {len(self.list_width) - 1}'
        self.current_size_main.value = f'Size: W {w},H {h}'
        self.update()
        self.page.update()

    def clickers(self,event:ft.TapEvent):
        if self.count_cl == 0:
            self.x = int(event.local_x)#thanks to ft.TapEvent I get coordinates
            self.y = int(event.local_y)
            self.update()
            self.page.update()
            self.count_cl = 1
        elif self.count_cl == 1:
            current_time = time.time()
            if current_time - self.last_click_time > self.double_click_time:
                self.double_click(event)
    def double_click(self,event:ft.TapEvent):
        self.x2 = int(event.local_x)
        self.y2 = int(event.local_y)
        if self.current_path:
            pillow_image = Image.open(self.current_path).convert('RGBA')
            width,height = pillow_image.size
            cont_width = self.image_container.width
            cont_height = self.image_container.height
            kof1 = width/cont_width
            kof2 = height/cont_height
            mask = Image.new('L',(width,height),255)
            draw = ImageDraw.Draw(mask) #I will paint on my mask
            if self.x < self.x2 and self.y < self.y2:
                draw.rectangle((self.x*kof1,self.y*kof2,self.x2*kof1,self.y2*kof2),fill = 0)
            else:
                self.page.show_snack_bar(
                    ft.SnackBar(ft.Text("The first point can't be less than second point", color='orange'), bgcolor=ft.colors.BLUE_100))
            new_image = Image.new('RGBA',(width,height),(0,0,0,0))
            new_image.paste(pillow_image,(0,0),mask)
            img_byte = io.BytesIO()
            new_image.save(img_byte,format="PNG")
            img_byte = img_byte.getvalue()
            encoded_image = base64.b64encode(img_byte).decode('ascii')
            self.image_container.content = ft.Image(src_base64 = encoded_image,fit = ft.ImageFit.CONTAIN)
            self.current_path = io.BytesIO(img_byte)
            self.list_pictures.append(self.current_path)
            self.list_width.append(self.image_container.width)
            self.list_height.append(self.image_container.height)
            self.movements.value = f'Movements : {len(self.list_width) - 1}'
        self.update()
        self.page.update()
    def change_fields(self,event):
        self.count_cl = 0
    def delete_dopping(self,event):
        self.help_count1 = 0
        self.dopping_image = None
        self.page.show_snack_bar(
            ft.SnackBar(ft.Text('You can choose the additional picture again!', color='orange'), bgcolor=ft.colors.BLUE_100))
        self.update()
        self.page.update()

    def save_img(self,event):
        if self.current_path:
            import random
            random_number = random.randint(1,50000)
            pillow_image = Image.open(self.current_path)
            pillow_image.save(f'new_image{random_number}.png',format="PNG")
            self.page.show_snack_bar(ft.SnackBar(ft.Text('Your picture was installed',color='orange'),bgcolor=ft.colors.BLUE_100))
        if self.count == 0:
            self.page.show_snack_bar(ft.SnackBar(ft.Text("You don't have a picture",color='orange'),bgcolor=ft.colors.BLUE_100))

    def build(self):
        return ft.Container(
            width=1400,
            height=600,
            content=ft.Row(
                controls=[
                    ft.Container(
                        expand=2.5,
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.IconButton(icon_color='green', icon=ft.icons.IMAGE_SEARCH, on_click=lambda event: self.file_picker.pick_files(allow_multiple=False, file_type=ft.FilePickerFileType.IMAGE)),
                                        ft.IconButton(icon=ft.icons.KEYBOARD_RETURN, on_click=self.return_image, icon_color='orange'),
                                        ft.ElevatedButton(width=100, height=40, text='Open', color=ft.colors.ORANGE, on_click=self.open),
                                        ft.ElevatedButton(width=100, height=40, text='Apply', color=ft.colors.ORANGE, on_click=self.resize_main),
                                        ft.Column(controls=[self.width_main, self.height_main]),
                                        ft.Row(controls=[self.current_size_main]),
                                    ],
                                    alignment=ft.MainAxisAlignment.START
                        ),
                        self.gesture1
                            ]
                        )
                    ),
                    ft.Container(
                        expand=1,
                        content=ft.Column(
                            controls=[
                                ft.Text('Filter:', color='orange'),
                                ft.ElevatedButton(width=180, height=50, text='Blurring', color=ft.colors.ORANGE, on_click=self.blur),
                                ft.ElevatedButton(width=180, height=50, text='Clarity', color=ft.colors.ORANGE, on_click=self.sharpen),
                                ft.ElevatedButton(width=180, height=50, text='Silvery', color=ft.colors.ORANGE, on_click=self.silver),
                                ft.ElevatedButton(width=180, height=50, text='Edge', color=ft.colors.ORANGE, on_click=self.strongedge),
                                ft.Text('Resize additional photo:', color='orange'),
                                self.size_doping,
                                ft.Row(controls=[
                                    ft.IconButton(icon_color='green', icon=ft.icons.PICTURE_IN_PICTURE, on_click=lambda event: self.file_picker2.pick_files(allow_multiple=False)),
                                    ft.IconButton(icon=ft.icons.DELETE, icon_color='red', on_click=self.delete_dopping)
                                ]),
                                self.resize_width, self.resize_height,
                                ft.ElevatedButton(text='Apply', width=180, height=50, color=ft.colors.ORANGE, on_click=self.resize_dop_img),
                                self.image_dopping_container,
                            ]
                        )
                    ),

                    ft.Container(
                        expand=1.5,
                        content=ft.Column(
                            controls=[
                                ft.Text('Automatically:', color='orange'),
                                self.radio_choice,
                                self.radio_colors,
                                self.radius,
                                ft.Text('Zoom(only horizontal):', color='orange'),
                                ft.Row(controls=[
                                    ft.IconButton(icon=ft.icons.ZOOM_IN, icon_color='green', on_click=self.zoom_plus),
                                    ft.IconButton(icon=ft.icons.ZOOM_OUT, icon_color='red', on_click=self.zoom_minus)
                                ]),
                                ft.Text('Rotate:', color='orange'),
                                ft.ElevatedButton(color=ft.colors.ORANGE, width=180, height=50, text='90', on_click=self.rotate_img_90),
                                ft.ElevatedButton(color=ft.colors.ORANGE, width=180, height=50, text='180', on_click=self.rotate_img_180),
                            ]
                        )
                    ),

                    ft.Container(
                        expand=1,
                        content=ft.Column(
                            controls=[
                                self.movements,
                                ft.Text('Manually(mask):', color='orange'),
                                ft.Row(controls=[self.user_text1, self.user_text2]),
                                ft.Row(controls=[self.user_text3, self.user_text4]),
                                ft.ElevatedButton(text='Apply', color=ft.colors.ORANGE, width=150, height=50, on_click=self.crop_rectangle),
                                ft.Text('Scalable help(100x100):', color='orange'),
                                self.radio,
                                ft.Text('Save:', color=ft.colors.ORANGE),
                                ft.IconButton(width=150, height=60, icon=ft.icons.SAVE, icon_color=ft.colors.ORANGE_500, on_click=self.save_img),
                            ]
                        )
                    )
                ]
            )
        )


    def pick_files(self, event):
         self.file_picker.pick_files(file_type=ft.FilePickerFileType.IMAGE)
    def pick_result(self, event: ft.FilePickerResultEvent):# event has information about picked files
        if self.count == 0:
            if event.files:
                self.current_path = event.files[0].path#список файлов
                for f in event.files:
                    self.image = ft.Image(
                        src=self.current_path,
                        fit=ft.ImageFit.CONTAIN,
                    )
                    self.list_pictures.append(self.current_path)
                    self.check_sizes()
                    self.image_container.content = self.image # put our image in container(it's the main)
                    self.count += 1
                    self.list_width.append(self.image_container.width)
                    self.list_height.append(self.image_container.height)
                    self.radio_choice.disabled = False
                    self.radio.disabled = False
                    self.update() #change design
                    self.page.update() #change all page
            else:
                self.page.show_snack_bar(ft.SnackBar(ft.Text("You chose nothing",color='orange'),bgcolor=ft.colors.BLUE_100))
        else:
             self.page.show_snack_bar(ft.SnackBar(ft.Text('You have already chosen the Image!',color='orange'),bgcolor=ft.colors.BLUE_100))
    def check_sizes(self):
        pillow_image = Image.open(self.current_path)
        width, height = pillow_image.size
        if width == height:
            self.number_w = 600
            self.number_h = 600
        elif width / height > 3.5:
            self.number_w = 600
            self.number_h = 150
        elif 3.5 >= width / height >= 2.9:
            self.number_w = 600
            self.number_h = 200
        elif 2.9 > width / height >= 2.6:
            self.number_w = 600
            self.number_h = 218
        elif 2.6 > width / height >= 2.3:
            self.number_w = 600
            self.number_h = 240
        elif 2.3 > width / height >= 2:
            self.number_w = 600
            self.number_h = 273
        elif 2 > width / height >= 1.8:
            self.number_w = 600
            self.number_h = 316
        elif 1.8 > width / height >= 1.6:
            self.number_w = 600
            self.number_h = 353
        elif 1.6 > width / height >= 1.3:
            self.number_w = 600
            self.number_h = 413
        elif 1.3 > width / height >= 1.1:
            self.number_w = 600
            self.number_h = 500
        elif 1.0 > width / height >= 0.8:
            self.number_w = 540
            self.number_h = 600
        elif 0.8 > width / height >= 0.6:
            self.number_w = 420
            self.number_h = 600
        elif 0.6 > width / height >= 0.4:
            self.number_w = 300
            self.number_h = 600
        elif 0.4 > width / height >= 0.2:
            self.number_w = 180
            self.number_h = 600
        elif width / height < 0.2:
            self.number_w = 80
            self.number_h = 600

        self.image_container.width = self.number_w
        self.image_container.height = self.number_h
        self.image_container.content = self.image  # put our image in container(it's the main)
        self.update()  # change design
        self.page.update()  # change all page
    def pick_result2(self,event:ft.FilePickerFileType.IMAGE):
        if self.count == 1:
            if event.files:
                self.dop_path = event.files[0].path
                for f in event.files:
                    self.dopping_image = ft.Image(src=self.dop_path,fit=ft.ImageFit.CONTAIN)
                    self.image_dopping_container.content = self.dopping_image
                    self.help_count1 += 1
                    self.update()
                    self.page.update()
def main(page: ft.Page):
    page.title = "Simplistic-PhotoRedactor"
    page.window_width = 1700
    page.window_height = 700
    page.theme_mode = 'dark'
    new = Redactor(page)
    page.overlay.extend([new.file_picker,new.file_picker2])
    page.add(new)
    page.update()

ft.app(target=main)


