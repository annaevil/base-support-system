<script setup lang="ts">
import { ref } from 'vue'
import Logo from "#/logo.svg"
import SoundRecorder from "@/components/SoundRecorder.vue"

const isMobile = ref(window.innerWidth <= 600)
const show = ref(false)

const showMore = () => {
  show.value = !show.value
}
</script>
<template>
  <div class="wrapper">
    <div class="flex__container">
      <div class="app">
        <button class="btn__more" v-if="isMobile" @click.prevent="showMore">{{ 'Показать иструкцию' }}</button>
        <div class="app__wrapper" v-show="show">
          <h2 class="app__title">Привет, наш талантливый друг!</h2>
          <p class="app__message">
            Спасибо, что помогаешь в работе над нашей программой! Вместе со ссылкой тебе был
            отправлен файл с нотами. Пожалуйста, приготовь ноты и попробуй выполнить
            следующую инструкцию:
          </p>
          <ul class="app__list">
            <li class="app__list-item">
              Выбери себе тихое место, иначе нашей программе будет тяжело слушать твою
              музыку.
            </li>
            <li class="app__list-item">
              Нажми на кнопку
              <span class="app__button">"начать запись"</span>, чтобы начать записывать свою
              игру.
            </li>
            <li class="app__list-item">Попробуй сыграть пьесу.</li>
            <li class="app__list-item">
              Когда закончишь, можешь остановить запись, нажми на кнопку
              <span class="app__button">"остановить запись"</span>.
            </li>
            <li class="app__list-item">Убедись, что появилась фраза "запись сохранена!"</li>
            <li class="app__list-item">
              Нажми на кнопку
              <span class="app__button">"отправить на проверку"</span>
              и дождись результата. Это может занять несколько секунд.
            </li>
          </ul>
          <p class="app__feedback">
            Программа умеет распознавать, какая нота была верная, а где была сделана ошибка.
            После того, как отправишь свою запись, ты увидишь на экране ноты. Там могут быть
            подсказки:
          </p>
          <ul class="app__notes">
            <li class="app__notes-item">
              Нота выделена <span class="red">красным</span> — значит, она была, скорее
              всего, неверная. Проверь еще раз!
            </li>
            <li class="app__notes-item">
              Нота выделена <span class="yellow">жёлтым</span> — обрати внимание на ритм в
              этом месте.
            </li>
            <li class="app__notes-item">
              Нота выделена <span class="green">зелённым</span> — молодец, сыграл ноту
              правильно.
            </li>
          </ul>
          <p class="app__contact">
            Мы всегда рядом, если есть какие-то вопросы или что-то не работает, пожалуйста,
            напиши нам в телеграм <a href="https://t.me/Alexismename">@alexismename</a> или
            на почту <a href=" mailto:topalidia@gmail.com">topalidia@gmail.com</a>.
            Приятного пользования!
          </p>
          <p class="app__team">Команда SM</p>
        </div>
      </div>
      <div class="play">
        <div class="play__logo">
          <Logo class="play__logo-item" />
        </div>
        <div class="play__title">
          <p>Начни запись и играй</p>
          <span>Играй четко. Убедись, что вокруг тихо.</span>
        </div>
        <div class="play__recorder">
          <SoundRecorder />
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped lang="scss">
.flex__container {
  display: flex;
  justify-content: center;
  column-gap: 20px;
  @media (max-width: 1200px) {
    flex-direction: column-reverse;
    gap: 30px;
  }
  .play {
    flex-basis: 400px;
    padding: 30px 10px;
    background: #fff;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
}
.app {
  flex-basis: 50%;
  padding: 10px 15px;
  background: #fff;
  border-radius: 15px;
  &__title {
    font-weight: bold;
    font-size: 25px;
    padding: 20px 0;
  }
  &__button {
    background: #ebdeff;
    border-radius: 2px;
    font-weight: bold;
  }
  &__message,
  &__feedback {
    font-weight: bold;
    padding-bottom: 20px;
  }
  &__list {
    position: relative;
    list-style: none;
    margin-bottom: 10px;
    padding-left: 20px;
    &-item {
      padding-bottom: 10px;
      &::before {
        content: "✔";
        position: absolute;
        left: 0;
        color: green;
      }
    }
  }
  &__notes {
    padding: 0 0 20px 18px;
    &-item {
      padding-bottom: 10px;
      .red {
        color: $red-color;
        font-weight: bold;
      }
      .yellow {
        color: $yellow-color;
        font-weight: bold;
      }
      .green {
        color: $green-color;
        font-weight: bold;
      }
    }
  }
  &__contact,
  &__team {
    font-weight: bold;
    line-height: 1.5;
  }
}
.play {
  padding: 30px 10px;
  &__logo {
    width: 100%;
    overflow: hidden;
    text-align: center;
  }
  &__title {
    text-align: center;
    padding: 20px 0 60px 0;
    p {
      font-weight: bold;
    }
  }
}
</style>
