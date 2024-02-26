<script lang="ts" setup>
import { ref, reactive, onMounted } from 'vue';
import axios from "axios";
import { useGptStore } from "@/stores/gpt"
import { ElLoading } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'

const data = reactive({
  responses: "",
  input: "",
  programmingLanguageList: "",
  platformList: "",
});

const { setGptResponse, getGptResponse } = useGptStore()

onMounted(() => {
  axios
    .get(import.meta.env.VITE_API_URL_BASE + import.meta.env.VITE_API_LANGUAGES)
    .then(response => {
      data.programmingLanguageList = response.data;
    });
  axios
      .get(import.meta.env.VITE_API_URL_BASE + import.meta.env.VITE_API_PLATFORMS)
      .then(response => {
        data.platformList = response.data;
      });
})

const url = import.meta.env.VITE_API_URL_BASE + import.meta.env.VITE_API_CHAT_GPT;
const requestApi = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  let submitFlg = false;
  await formEl.validate((valid, fields) => {
    if (valid) {
      console.log('submit!')
      submitFlg = true;
    } else {
      console.log('error submit!', fields)
      submitFlg = false;
    }
  })

  if (!submitFlg) return

  const loadingInstance = ElLoading.service({ fullscreen: true })
  // リクエスト(入力項目をjson)
  const result = await axios.post(url,
    {
      prompt: {
        appOverview: ruleForm.appOverview,
        programmingLanguage: ruleForm.programmingLanguage,
        platform: ruleForm.platform,
        useDatabase: ruleForm.useDatabase,
        useCloud: ruleForm.useCloud
      }
    }
  ).then((response) => {
    setGptResponse(response.data)
    data.responses = getGptResponse()
    loadingInstance.close()
  }).catch((error) => {
    ElMessage({
      message: 'ChatGPT実行に失敗しました。',
      type: 'error',
    })
    console.log(error.response);
    loadingInstance.close()
  });
};

interface RuleForm {
  appOverview: string
  programmingLanguage: string
  platform: string
  useDatabase: boolean
  useCloud: boolean
}

const formSize = ref('default')
const ruleFormRef = ref<FormInstance>()
const ruleForm = reactive<RuleForm>({
  appOverview: '',
  programmingLanguage: 1,
  platform: 1,
  useDatabase: false,
  useCloud: false,
})

const rules = reactive<FormRules<RuleForm>>({
  appOverview: [
    { required: true, message: 'アプリ概要を入力して下さい', trigger: 'blur' },
    { max: 50, message: 'アプリ概要を50文字以内で入力してください', trigger: 'blur' }
  ],
})

const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
  data.responses = ""
};

</script>

<template>
  <el-card shadow="never" class="w-full max-w-md" :body-style="{ padding: 20 }">
    <div class="m-8 text-center">
      <el-link href="https://element-plus.org/en-US/" :underline="false" class="m-0">
        <img src="https://element-plus.org/images/element-plus-logo.svg" class="block w-[120px] h-[28px]"
          alt="Element Plus" />
      </el-link>
    </div>
    <el-form ref="ruleFormRef" :rules="rules" :model="ruleForm" :size="formSize" label-position="top">
      <el-form-item label="作りたいアプリ概要を入力" prop="appOverview">
        <el-input v-model="ruleForm.appOverview" size="large" />
      </el-form-item>
      <el-form-item label="言語を入力" prop="programmingLanguage">
        <el-select v-model="ruleForm.programmingLanguage" value-key="id">
          <el-option v-for="programmingLanguage in data.programmingLanguageList" :key="programmingLanguage.id"
            :label="`${programmingLanguage.dispName}`" :value="programmingLanguage.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="プラットフォームを入力" prop="platform">
        <el-select v-model="ruleForm.platform" value-key="id">
          <el-option v-for="platform in data.platformList" :key="platform.id" :label="`${platform.dispname}`"
            :value="platform.id" />
        </el-select>
      </el-form-item>
      <el-form-item class="flex justify-between mb-2" prop="useDatabase">
        <el-checkbox v-model="ruleForm.useDatabase" label="DBを使用する" size="large" />
      </el-form-item>
      <el-form-item class="flex justify-between mb-2" prop="useCloud">
        <el-checkbox v-model="ruleForm.useCloud" label="クラウドを使用する" size="large" />
      </el-form-item>
      <el-button @click="requestApi(ruleFormRef)" type="primary" size="large" class="w-full">作成</el-button>
      <el-button @click="resetForm(ruleFormRef)" size="large" class="w-full">リセット</el-button>
    </el-form>
  </el-card>
  <el-card v-if="data.responses !== ''" shadow="never" class="w-full max-w-md margin">
    <div class="response__container">
      <div class="response">
        <div class="text">{{ data.responses.content }}</div>
      </div>
    </div>
  </el-card>
</template>

<style scoped>
.margin {
  margin-top: 20px;
}

.response__container .response {
  position: relative;
  display: block;
  margin: 10px 0;
  margin-top: -5px;
  max-width: 95%;
  float: left;
  margin-right: 5px;
  /* 5px */
  clear: both;
}

.response__container .response .text {
  padding: 10px;
  border-radius: 10px;
  margin: 0;
  background-color: #D6D9D7;
  /* 背景色 自分 */
  color: #000000;
  /* 文字色 */
  font-size: 15px;
  /* 文字サイズ */
  white-space: pre-wrap;
  /* 改行 */
}
</style>
