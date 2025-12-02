<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const currentWord = ref('')
const targetWord = ref('')
const nextWords = ref([])
const score = ref(100)
const steps = ref(0)
const startTime = ref(0)

const fetchNextWords = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/get_next_words/${currentWord.value}`)
    nextWords.value = response.data.next_words
  } catch (error) {
    console.error('Hiba történt az adatok lekérésekor:', error)
  }
}

const fetchRandomWords = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/get_random_words')
    currentWord.value = response.data.start_word
    targetWord.value = response.data.target_word
    steps.value = 0
    score.value = 100
    startTime.value = Date.now()
    fetchNextWords()
  } catch (error) {
    console.error('Hiba történt a random szavak lekérésekor:', error)
  }
}

const selectWord = (word) => {
  currentWord.value = word
  steps.value++
  fetchNextWords()

  if (word === targetWord.value) {
    const timeTaken = (Date.now() - startTime.value) / 1000 // másodperc
    score.value -= steps.value * 2 // minden extra lépés -2 pont
    score.value -= Math.floor(timeTaken) // minden másodperc -1 pont
    alert(`Gratulálok! Végső pontszám: ${score.value}`)
    fetchRandomWords() // új játék kezdése
  }
}

onMounted(() => {
  fetchRandomWords()
})

</script>

<template>
  <div>
    <h2>Jelenlegi szó: {{ currentWord }}</h2>
    <h2>Célszó: {{ targetWord }}</h2>
    <!--<h3>Pontszám: {{ score }}</h3>-->
    <button v-for="word in nextWords" :key="word" @click="selectWord(word)">
      {{ word }}
    </button>
  </div>
</template>

<style scoped>
button {
  margin: 5px;
  padding: 10px;
  background-color: lightblue;
  border: none;
  cursor: pointer;
}
</style>
