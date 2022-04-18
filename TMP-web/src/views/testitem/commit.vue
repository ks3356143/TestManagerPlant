<template>
  <div class="app-container">
    <el-header>
      <el-page-header @back="goback" content="测试项表单" />
    </el-header>
    <el-main>
      <el-form
        :model="requestForm"
        :rules="requestRules"
        ref="ruleForm"
        label-width="100px"
      >
        <el-form-item label="测试项标题" prop="title">
          <el-input
            v-model="requestForm.title"
            clearable
            placeholder="请输入测试项标题"
            style="width: 300px"
          />
        </el-form-item>
        <el-form-item label="配置项/系统ID" prop="appId">
          <el-select
            v-model="requestForm.appId"
            filterable
            remote
            reserve-keyword
            placeholder="支持远程搜索测试项名称和appId"
            :remote-method="remoteMethod"
            :loading="appIdloading"
            @change="appSelected"
          >
            <el-option
              v-for="item in appList"
              :key="item.id"
              :label="item.label"
              :value="item.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="测试人员" prop="tester">
          <el-input
            v-model="requestForm.tester"
            placeholder="测试人员"
            style="width: 350px"
          ></el-input>
        </el-form-item>
        <el-form-item label="版本号" prop="version">
          <el-input
            v-model="requestForm.version"
            placeholder="请输入版本号"
            style="width: 350px"
          ></el-input>
        </el-form-item>
        <el-form-item label="测试类型" prop="type">
          <el-select
            v-model="requestForm.type"
            clearable
            placeholder="请选择测试类型"
            style="width: 300px"
          >
            <el-option
              v-for="item in opsType"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="测试项名称" prop="name">
          <el-input
            v-model="requestForm.name"
            placeholder="请输入测试项名称"
            style="width: 350px"
          ></el-input>
        </el-form-item>
        <el-form-item label="测试项标识" prop="ident">
          <el-input
            v-model="requestForm.ident"
            placeholder="请输入测试项标识"
            style="width: 350px"
          ></el-input>
        </el-form-item>
        <el-form-item label="测试项描述" prop="comm">
          <el-input
            v-model="requestForm.comm"
            placeholder="请输入测试描述"
            style="width: 350px"
            type="textarea"
            :rows="5"
          ></el-input>
        </el-form-item>
        <el-form-item label="测试方法" prop="method">
          <el-input
            v-model="requestForm.method"
            placeholder="请输入测试方法"
            style="width: 350px"
            type="textarea"
            :rows="3"
          ></el-input>
        </el-form-item>
        <el-form-item label="追踪文档名称" prop="refe">
          <el-input
            v-model="requestForm.refe"
            placeholder="请输入追踪文档名"
            style="width: 350px"
          ></el-input>
        </el-form-item>
        <el-form-item label="追踪文档章节号" prop="refhao">
          <el-input
            v-model="requestForm.refhao"
            placeholder="请输入追踪文档章节号"
            style="width: 350px"
          ></el-input>
        </el-form-item>
        <el-form-item label="追踪文档章节名称" prop="refname">
          <el-input
            v-model="requestForm.refname"
            placeholder="请输入追踪文档章节名称"
            style="width: 350px"
          ></el-input>
        </el-form-item>
        <el-form-item label="执行优先级" prop="shun">
          <el-select
            v-model="requestForm.shun"
            clearable
            placeholder="请选择执行优先级"
            style="width: 300px"
          >
            <el-option
              v-for="itemS in opsShun"
              :key="itemS.value"
              :label="itemS.label"
              :value="itemS.value"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="测试内容和方法" prop="caseitem">
          <el-input
            v-model="requestForm.caseitem"
            placeholder="请输入测试内容和方法"
            style="width: 350px"
            type="textarea"
            :rows="12"
          ></el-input>
        </el-form-item>
        <el-form-item label="测试通过准则" prop="passitem">
          <el-input
            v-model="requestForm.passitem"
            placeholder="请输入测试通过准则"
            style="width: 350px"
            type="textarea"
            :rows="12"
          ></el-input>
        </el-form-item>
        <el-form-item label="创建人" prop="createUser">
          <el-input
            v-model="requestForm.createUser"
            placeholder="请输入测试项标识"
            style="width: 350px"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">立即创建</el-button>
          <el-button @click="onCancel">取消</el-button>
        </el-form-item>
      </el-form>
    </el-main>
  </div>
</template>

<script>
import { apiAppsId } from "@/api/apps";
import { reqCreate } from "@/api/test";
import store from "@/store";
export default {
  name: "commit",
  data() {
    return {
      op_user: store.getters.name,
      testAction: "",
      appIdloading: false,
      requestForm: {
        title: "",
        appId: "",
        tester: "",
        version: "",
        type: "",
        name: "",
        ident: "",
        comm: "",
        method: "",
        refe: "",
        refhao: "",
        refname: "",
        shun: "",
        caseitem: "",
        passitem: "",
        createUser: "",
      },
    };
  },
};
</script>

<style></style>
