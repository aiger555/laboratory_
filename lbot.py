import telebot
import pandas
import telebot
import aioschedule as schedule


# import parser

class KivanoBot:
    help_text = '''
    /categories - выдать названия всех категорий.
    /categories - {название категории} выдать товары этой категории. (название и ссылку)
    /product - {название продукта} выдать информацию о данном товаре. (название, название категории, ссылка)
    '''
    kivanos = pandas.read_csv('kivano.csv')
    kivanoset = set(kivanos.category_name.to_list())
    kivanoset2 = set(kivanos.title)

    def show(self, args):
        if len(args) <= 0:
            return '\n'.join(self.kivanoset)
        else:
            advert = f'{args}'
            if advert not in self.kivanoset:
                return f'{args} - Not exist'
            else:
                advert_new = self.kivanos[self.kivanos.category_name == advert]
                advert_new = advert_new[['title', 'link']][:5].to_string()
            return advert_new

    def show_products(self, word):
        if word not in self.kivanoset2:
            return f'{word} doesn\'t exist'
        else:
            product = self.kivanos[self.kivanos.title == word]
            product = product[['category_name', 'title', 'link']].to_string()
            return product


TOKEN = '1786741150:AAF9gKI8UIThbhCqxeGTovSzBtDwteV3V_M'
bot = telebot.TeleBot(TOKEN)
lbot = KivanoBot()


@bot.message_handler(commands=['start', 'help'])
def show(message):
    bot.send_message(message.chat.id, lbot.help_text)


@bot.message_handler(commands=['categories'])
def fractions(message):
    args = message.text[10:]
    bot.send_message(message.chat.id, lbot.show(args))


@bot.message_handler(commands=['product'])
def fractions(message):
    args = message.text[10:]
    bot.send_message(message.chat.id, lbot.show_products(args))


if __name__ == '__main__':
    bot.polling()
