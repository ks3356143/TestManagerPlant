<template>
  <div class="app-container">
    <el-dialog title="添加项目" :visible.sync="dialogProductShow">
      <el-form :model="product">
        <el-form-item label="项目类型" label-width="100px">
          <el-input
            v-model="product.type"
            placeholder="请输入项目类型"
            style="width: 90%"
          ></el-input>
        </el-form-item>
        <el-form-item label="项目唯一代号" label-width="100px">
          <el-input
            v-model="product.keyCode"
            placeholder="请输入唯一代号"
            style="width: 90%"
          ></el-input>
        </el-form-item>
        <el-form-item label="项目名称" label-width="100px">
          <el-input
            v-model="product.title"
            placeholder="请输入项目名称"
            style="width: 90%"
          ></el-input>
        </el-form-item>
        <el-form-item label="测试人员" label-width="100px">
          <el-input
            v-model="product.tester"
            placeholder="请输入该项目测试人员"
            style="width: 90%"
          ></el-input>
        </el-form-item>
        <el-form-item label="项目阶段" label-width="100px">
          <el-input
            v-model="product.step"
            placeholder="请输入目前项目阶段"
            style="width: 90%"
          ></el-input>
        </el-form-item>
        <el-form-item label="客户名称" label-width="100px">
          <el-input
            v-model="product.customer"
            placeholder="请输入客户名称"
            style="width: 90%"
          ></el-input>
        </el-form-item>
        <el-form-item label="销售人员" label-width="100px">
          <el-input
            v-model="product.seller"
            placeholder="请输入该项目销售人员"
            style="width: 90%"
          ></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogProductShow = false">取消</el-button>
        <el-button type="primary" @click="pCreate()">确定</el-button>
      </span>
    </el-dialog>
    <div class="filter-container">
      <el-button
        type="primary"
        icon="el-icon-plus"
        style="float: right"
        @click="dialogProduct()"
        >新增项目</el-button
      >
    </div>
    <el-table :data="tableData">
      <el-table-column prop="id" label="编号" />
      <el-table-column prop="type" label="项目类型" />
      <el-table-column prop="keyCode" label="唯一标识" />
      <el-table-column prop="title" label="项目名" />
      <el-table-column prop="tester" label="测试负责人" />
      <el-table-column prop="step" label="阶段" />
      <el-table-column prop="customer" label="客户单位" />
      <el-table-column prop="seller" label="销售人员" />
      <el-table-column prop="update" label="更新时间" show-overflow-tooltip="" />
      <el-table-column prop="begintime" label="开始时间" show-overflow-tooltip="" />
    </el-table>
  </div>
</template>

<script>
import { apiProductList, apiProductCreate } from "@/api/product";
import store from "@/store";
export default {
  name: "Product", // 页面名称
  // data() 数据\属性，固定return中配置
  data() {
    return {
      tableData: [],
      //定义项目添加数据
      op_user: store.getters.name,
      //定义项目参数
      product: {
        id: undefined,
        type: undefined,
        keyCode: undefined,
        title: undefined,
        tester: this.op_user,
        step: undefined,
        customer: undefined,
        seller: undefined,
      },
      //定义控制嵌套表单显示与取消
      dialogProductShow: false,
    };
  },
  // 页面生命周期中的创建阶段调用
  created() {
    // 调用methods的方法，即初次加载就请求数据
    this.getProductList();
  },
  methods: {
    // getProductList自定义方法名，提供其他地方调用this.getProductList
    getProductList() {
      // 固定格式调用api配置方法，并将返回结果回调给response
      apiProductList().then((response) => {
        // console.log（）是调试打印，可以在chrome开发者工具中查看
        console.log(response.data);
        // 将返回的结果赋值给变量 tableData
        this.tableData = response.data;
      });
    },
    //dialogProduct按钮方法，第一步实现数据情况，然后弹出对话框变量为True
    dialogProduct() {
      //初始化空状态
      (this.product.id = undefined),
        (this.product.type = ""),
        (this.product.keyCode = ""),
        (this.product.title = ""),
        (this.product.tester = ""),
        (this.product.step = ""),
        (this.product.customer = ""),
        (this.product.seller = ""),
        //弹窗变量显示设置为true
        (this.dialogProductShow = true);
      console.log("点击了新增项目按钮");
    },
    pCreate() {
      apiProductCreate(this.product).then((response) => {
        this.$notify({
          title: "成功",
          type: "success",
          message: "成功添加项目一个",
        });
      });
      //将对话框关闭
      this.dialogProductShow = false;
      //刷新下项目列表
      this.getProductList();
    },
  },
};
</script>

<style scoped></style>
