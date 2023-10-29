from aiogram import Bot, Dispatcher, types, executor
import copy
from typing import Optional

from matrix import Matrix, MatrixError, parse_matrix

bot = Bot('6714468247:AAG14Qbit7kcN1uYvDLcJxyI2TYvcw7MTKM')
dp_bot = Dispatcher(bot)

MULT_CMD = 'Умножение'
TRANS_CMD = 'Транспонировать'
SIZE_CMD = 'Размерность'
ADD_CMD = 'Сложение'
POW_CMD = 'Возведение в степень'

CMD_LIST = [MULT_CMD, TRANS_CMD, SIZE_CMD, ADD_CMD, POW_CMD]

first_matrix = None
second_matrix = None
prev_cmd = None


@dp_bot.message_handler(commands=['start'])
async def start(message: types.Message):
    but = types.ReplyKeyboardMarkup()

    for cmd in CMD_LIST:
        but.add(types.KeyboardButton(cmd))
    await message.answer('Привет! Выберите действие', reply_markup=but)
    # dp_bot.register_message_handler(message, )


@dp_bot.message_handler()
async def button(message: types.Message):
    but = types.ReplyKeyboardMarkup()

    for cmd in CMD_LIST:
        but.add(types.KeyboardButton(cmd))

    text = message['text']
    if text == MULT_CMD or prev_cmd == MULT_CMD:
        await mul(text, message, but)
    elif text == TRANS_CMD or prev_cmd == TRANS_CMD:
        await transpose(text, message, but)
    elif text == SIZE_CMD or prev_cmd == SIZE_CMD:
        await size(text, message, but)
    elif text == ADD_CMD or prev_cmd == ADD_CMD:
        await add(text, message, but)
    elif text == POW_CMD or prev_cmd == POW_CMD:
        await pow(text, message, but)
    else:
        await message.answer('Отправь мне матрицу в формате [[a, b], [c, d]]', reply_markup=but)




async def mul(text: str, message: types.Message, but):
    global prev_cmd, first_matrix, second_matrix
    prev_cmd = MULT_CMD

    if first_matrix is None:
        if text == MULT_CMD:
            await message.answer('введите матрицу 1')
            return
        else:
            first_matrix = parse_matrix(text)
            if first_matrix is None:
                await message.answer('Матрица некорректна. Отправь мне матрицу в формате [[a, b], [c, d]]')
                return
            await message.answer('успешно считали матрицу 1, введите матрицу 2 или целое число')
            return

    if second_matrix is None:
        second_matrix = parse_matrix(text)
        if second_matrix is None:
            await message.answer('Матрица некорректна. Отправь мне матрицу в формате [[a, b], [c, d]]')
            return
        try:
            result = first_matrix * second_matrix
            await message.answer('результат умножения:\n' + str(result), reply_markup=but)
        except MatrixError:
            await message.answer('Матрицы некорректны для умножения. Не соответствующие размеры матриц')

        first_matrix = None
        second_matrix = None
        prev_cmd = None

        return

async def transpose(text: str, message: types.Message, but):
    global prev_cmd, first_matrix
    prev_cmd = TRANS_CMD
    if first_matrix is None:
        if text == TRANS_CMD:
            await message.answer('введите матрицу')
            return
        else:
            first_matrix = parse_matrix(text)
            if first_matrix is None:
                await message.answer('Матрица некорректна. Отправь мне матрицу в формате [[a, b], [c, d]]')
                return
            await message.answer('успешно считали матрицу')

            result = first_matrix.transpose()
            print(result)

            await message.answer('результат транспонирования:\n' + str(result), reply_markup=but)

            first_matrix = None
            prev_cmd = None

            return


async def size(text: str, message: types.Message, but):
    global prev_cmd, first_matrix
    prev_cmd = SIZE_CMD

    if first_matrix is None:
        if text == SIZE_CMD:
            await message.answer('введите матрицу')
            return
        else:
            first_matrix = parse_matrix(text)
            if first_matrix is None:
                await message.answer('Матрица некорректна. Отправь мне матрицу в формате [[a, b], [c, d]]')
                return
            await message.answer('успешно считали матрицу')

            result = first_matrix.size()
            print(result)

            await message.answer('размерность:\n' + str(result), reply_markup=but)

            first_matrix = None
            prev_cmd = None
            return

async def add(text: str, message: types.Message, but):
    global prev_cmd, first_matrix, second_matrix
    prev_cmd = ADD_CMD

    if first_matrix is None:
        if text == ADD_CMD:
            await message.answer('введите матрицу 1')
            return
        else:
            first_matrix = parse_matrix(text)
            if first_matrix is None:
                await message.answer('Матрица некорректна. Отправь мне матрицу в формате [[a, b], [c, d]]')
                return
            await message.answer('успешно считали матрицу 1, введите матрицу 2')
            return

    if second_matrix is None:
        second_matrix = parse_matrix(text)
        if second_matrix is None:
            await message.answer('Матрица некорректна. Отправь мне матрицу в формате [[a, b], [c, d]]')
            return
        try:
            result = first_matrix + second_matrix
            await message.answer('результат сложения:\n' + str(result), reply_markup=but)
        except MatrixError:
            await message.answer('Матрицы некорректны для сложения. Разные размеры матриц')

        first_matrix = None
        second_matrix = None
        prev_cmd = None

        return

async def pow(text: str, message: types.Message, but):
    global prev_cmd, first_matrix
    prev_cmd = POW_CMD

    if first_matrix is None:
        if text == POW_CMD:
            await message.answer('введите матрицу')
            return
        else:
            first_matrix = parse_matrix(text)
            if first_matrix is None:
                await message.answer('Матрица некорректна. Отправь мне матрицу в формате [[a, b], [c, d]]')
                return
            await message.answer('успешно считали матрицу, введите число')
            return

    try:
        number = float(text)
    except Exception:
        await message.answer('Необходимо число')
    try:
        result = first_matrix ** number
        await message.answer('результат возведения в степень:\n' + str(result), reply_markup=but)
    except MatrixError:
        await message.answer('Матрица некорректна для возведения в степень. Можно возвести в степень только квадратную матрицу')
    first_matrix = None
    prev_cmd = None
    return

executor.start_polling(dp_bot)


