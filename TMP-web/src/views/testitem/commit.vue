<template>
  <div class="app-container">
    <el-header>
      <el-page-header @back="goBack" content="测试项添加表单"> </el-page-header>
    </el-header>
    <el-main>
      <el-form
        :model="requestForm"
        :rules="requestRules"
        ref="ruleForm"
        label-width="150px"
      >
        <el-form-item label="测试项标题" prop="title">
          <el-input
            v-model="requestForm.title"
            clearable
            placeholder="请输入测试项标题"
            style="width: 350px"
          />
        </el-form-item>
        <el-form-item label="配置项/系统ID" prop="appId">
          <el-select
            style="width: 350px"
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
              v-for="item in appIdList"
              :key="item.id"
              :label="item.name"
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
import { apiAppsIds } from "@/api/apps";
import { reqCreate } from "@/api/test";
import store from "@/store";
export default {
  name: "commit",
  data() {
    return {
      op_user: store.getters.name,
      testAction: "ADD",
      appIdloading: false,
      requestForm: {
        id: "undefined",
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
        createUser: store.getters.name,
      },
      requestRules: {
        title: [
          {
            required: true,
            message: "请输入测试项标题",
            trigger: "blur",
          },
          {
            min: 2,
            max: 20,
            message: "长度大于2个字符小于20个字符",
            trigger: "blur",
          },
        ],
        appId: [
          {
            required: true,
            message: "请选择所属配置项或者系统",
            trigger: "change",
          },
        ],
        tester: [
          {
            required: true,
            message: "请输入测试人员名称",
            trigger: "change",
          },
        ],
        version: [
          {
            required: true,
            message: "请输入版本号",
            trigger: "change",
          },
        ],
        type: [
          {
            required: true,
            message: "请选择测试类型",
            trigger: "change",
          },
        ],
        name: [
          {
            required: true,
            message: "请输入测试项名称",
            trigger: "change",
          },
        ],
        ident: [
          {
            required: true,
            message: "请输入测试项标识（4个字母标识）",
            trigger: "blur",
          },
        ],
        comm: [
          {
            required: true,
            message: "请输入测试项描述",
            trigger: "blur",
          },
        ],
        method: [
          {
            required: true,
            message: "请输入测试方法",
            trigger: "blur",
          },
        ],
        refe: [
          {
            required: true,
            message: "请输入追踪需求文档名称",
            trigger: "change",
          },
        ],
        refhao: [
          {
            required: true,
            message: "请输入追踪需求文档章节号",
            trigger: "change",
          },
        ],
        refname: [
          {
            required: true,
            message: "请输入追踪需求文档章节名称",
            trigger: "change",
          },
        ],
        shun: [
          {
            message: "请选择测试优先级别",
            trigger: "change",
          },
        ],
        caseitem: [
          {
            required: true,
            message: "请输入测试内容和方法",
            trigger: "blur",
          },
        ],
        passitem: [
          {
            required: true,
            message: "请输入通过准则（对应测试内容和方法的序号填写）",
            trigger: "blur",
          },
        ],
      },
      opsType: [
        { label: "功能测试", value: "1" },
        { label: "接口测试", value: "2" },
        { label: "性能测试", value: "3" },
        { label: "文档审查", value: "4" },
        { label: "代码审查", value: "5" },
        { label: "静态分析", value: "6" },
        { label: "余量测试", value: "7" },
        { label: "人机交互界面", value: "8" },
        { label: "安全测试", value: "9" },
        { label: "恢复性测试", value: "10" },
        { label: "边界测试", value: "11" },
        { label: "强度测试", value: "12" },
        { label: "兼容性测试", value: "13" },
        { label: "安装性测试", value: "14" },
        { label: "逻辑测试", value: "15" },
      ],
      opsShun: [
        { label: "高", value: "高" },
        { label: "中", value: "中" },
        { label: "低", value: "低" },
      ],
      appIdList: [],
    };
  },
  mounted() {
    if (this.$route.params.action) {
      this.testAction = this.$route.params.action;
    }
    console.log(this.testAction);
  },
  methods: {
    goBack() {
      console.log("点击了返回按钮");
      this.$router.push({ path: "/tmp/testitem" });
    },
    remoteMethod(query) {
      if (query !== "") {
        this.appIdloading = true;
        setTimeout(() => {
          apiAppsIds(query).then((resp) => {
            this.appIdList = resp.data;
          });
          this.appIdloading = false;
        }, 200);
      } else {
        this.appIdList = [];
      }
    },
    appSelected() {
      //判断获取应用的其他信息
      for (let it in this.appIdList) {
        if (this.appIdList[it].id === this.requestForm.appId) {
          //判断字符为空时候，即认为没有人工输入
          if (!this.requestForm.tester) {
            this.requestForm.tester = this.appIdList[it].updateUser;
          }
        }
      }
    },
    onSubmit() {
      this.$refs["ruleForm"].validate((valid) => {
        if (valid) {
          if (this.testAction === "ADD") {
            this.requestForm.id = undefined;
            this.requestForm.createUser = this.op_user;
            reqCreate(this.requestForm).then((response) => {
              this.$notify({
                title: "成功",
                message: this.testAction === "ADD" ? "添加成功" : "修改成功",
                type: "success",
              });
              //回到testitem页面
              this.$router.push({ path: "/tmp/testitem", params: { needUp: true } });
            });
          }
        } else {
          return false;
        }
      });
    },
    onCancel() {
      this.$router.push({ path: "/tmp/testitem" });
    },
  },
};
</script>

<style></style>
