<template>
  <div class="audio">
    <div v-if="isRecording" class="recording-animation">
      <div class="bar" v-for="n in 10" :key="n"></div>
    </div>
    <audio v-if="audioUrl" :src="audioUrl" controls></audio>

    <p v-if="errors" class="error">
      <span class="font-medium">{{ errors }}</span>
    </p>

    <div class="audio__btns">
      <div class="audio__btns-items">
        <button 
          @click="startRecording" 
          :disabled="isRecording" 
          class="btn play__btn"
        >
          {{ isRecording ? "Идет запись..." : "Начать запись" }}
        </button>
        <button 
          @click="stopRecording" 
          :disabled="!isRecording" 
          class="btn stop__btn"
        >
          Остановить запись
        </button>
      </div>
      <button 
        @click="submitAudio" 
        :disabled="!audioUrl"
        class="btn submit__btn"
      >
        Отправить на проверку
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue"

const mediaRecorder = ref<MediaRecorder | null>(null)
const audioChunks = ref<Blob[]>([])
const audioUrl = ref<string | null>(null)
const isRecording = ref(false)
const errors = ref<string | null>(null)

const startRecording = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    mediaRecorder.value = new MediaRecorder(stream, { mimeType: "audio/webm" }) 

    mediaRecorder.value.ondataavailable = (event: BlobEvent) => {
      audioChunks.value.push(event.data)
    }

    mediaRecorder.value.onstop = () => {
      const audioBlob = new Blob(audioChunks.value, { type: "audio/webm" })
      audioUrl.value = URL.createObjectURL(audioBlob)
      audioChunks.value = []
    }

    mediaRecorder.value.start()
    isRecording.value = true
  } catch (error) {
    errors.value = "Ошибка при доступе к микрофону: " + (error as Error).message
  }
}

const stopRecording = () => {
  mediaRecorder.value?.stop()
  isRecording.value = false
}

const submitAudio = async () => {
  const formData = new FormData()
  const audioBlob = new Blob(audioChunks.value, { type: "audio/webm" })
  formData.append("audio", audioBlob, "recording.webm")

  try {
    const response = await fetch("/results/", {
      method: "POST",
      body: formData,
    })

    if (!response.ok) {
      errors.value = "Ошибка при отправке на сервер"
    } else {
      audioUrl.value = null
    }
  } catch (error) {
    errors.value = "Ошибка при отправке: " + (error as Error).message
  }
}
</script>

<style scoped lang="scss">
.audio {
  display: flex;
  flex-direction: column;
  align-items: center;

  &__btns {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 0;
    gap: 20px;

    &-items {
      display: flex;
      gap: 15px;
    }
  }

  .btn {
    border-radius: 7px;
  }

  .play__btn {
    background-color: #00b459;
    color: white;
    &:hover {
      background-color: #02ad57;
      box-shadow: inset 0 0 10px #064800;
    }

    &:disabled {
      background-color: #d3d3d3;
      color: #8a8a8a;
      cursor: not-allowed;
    }
  }

  .stop__btn {
    background: none;
    border: 1px solid #a1a1a1;
    color: #a1a1a1;

    &:hover {
      box-shadow: inset 0 0 10px #aeaeae;
    }

    &:disabled {
      border-color: #d3d3d3;
      color: #d3d3d3;
      cursor: not-allowed;
    }
  }

  .submit__btn {
    background-color: #a400e5;
    &:hover {
      background-color: #9901d4;
      box-shadow: inset 0 0 10px #610087;
    }
  }
}

.recording-animation {
  display: flex;
  gap: 4px;
  margin-bottom: 20px;
  transform: rotate(180deg);
  height: 30px;

  .bar {
    width: 6px;
    height: 20px;
    background-color: #666;
    animation: sound 0ms -800ms linear infinite alternate;
    transform-origin: bottom;
  }

  @keyframes sound {
    0% {
       opacity: .35;
        height: 3px; 
    }
    100% {
        opacity: 1;       
        height: 28px;        
    }
}

.bar:nth-child(1)  { left: 1px; animation-duration: 474ms; }
.bar:nth-child(2)  { left: 5px; animation-duration: 433ms; }
.bar:nth-child(3)  { left: 9px; animation-duration: 407ms; }
.bar:nth-child(4)  { left: 13px; animation-duration: 458ms; }
.bar:nth-child(5)  { left: 17px; animation-duration: 400ms; }
.bar:nth-child(6)  { left: 21px; animation-duration: 427ms; }
.bar:nth-child(7)  { left: 25px; animation-duration: 441ms; }
.bar:nth-child(8)  { left: 29px; animation-duration: 419ms; }
.bar:nth-child(9)  { left: 33px; animation-duration: 487ms; }
.bar:nth-child(10) { left: 37px; animation-duration: 442ms; }
}
</style>
