<template>
  <div class="app-container">
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
import { apiProductList } from "@/api/product";
export default {
  name: "Product", // 页面名称
  // data() 数据\属性，固定return中配置
  data() {
    return {
      tableData: [],
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
  },
};
</script>

<style scoped></style>
