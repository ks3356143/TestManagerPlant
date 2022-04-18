<template>
  <div class="app-container">
    <div class="filter-container">
      <el-form :inline="true" :model="search">
        <el-form-item label="归属项目">
          <el-select v-model="search.productId">
            <el-option value="" label="所有" />
            <el-option
              v-for="item in optsProduct"
              :key="item.id"
              :label="item.title"
              :value="item.id"
            >
              <span style="float: left">{{ item.keyCode }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">{{
                item.title
              }}</span></el-option
            >
          </el-select>
        </el-form-item>
        <el-form-item label="配置项/系统ID">
          <el-input
            v-model="search.appId"
            placeholder="配置项/系统ID查询"
            style="width: 200px"
            clearable
          />
        </el-form-item>
        <el-form-item label="测试负责人">
          <el-input
            v-model="search.tester"
            placeholder="支持模糊查询"
            style="width: 210px"
            clearable
          />
        </el-form-item>
        <el-form-item label="测试类型">
          <el-select v-model="search.type">
            <el-option value="" label="所有" />
            <el-option value="1" label="功能" />
            <el-option value="2" label="接口" />
            <el-option value="3" label="性能" />
            <el-option value="4" label="文档审查" />
            <el-option value="5" label="代码审查" />
            <el-option value="6" label="静态分析" />
            <el-option value="7" label="余量" />
            <el-option value="8" label="人机交互界面" />
            <el-option value="9" label="安全性" />
            <el-option value="10" label="恢复性" />
            <el-option value="11" label="边界" />
            <el-option value="12" label="强度" />
            <el-option value="13" label="兼容" />
            <el-option value="14" label="安装性" />
            <el-option value="15" label="逻辑" />
          </el-select>
        </el-form-item>
        <el-form-item label="标识搜索">
          <el-input
            v-model="search.ident"
            placeholder="支持模糊查询"
            style="width: 210px"
            clearable
          />
        </el-form-item>
        <el-form-item label="时间范围">
          <el-date-picker
            v-model="search.pickTime"
            type="datetimerange"
            :picker-options="pickerOptions"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            align="right"
          >
          </el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" plain @click="searchClick()">查询</el-button>
        </el-form-item>
      </el-form>
      <el-button
        type="primary"
        icon="el-icon-plus"
        style="float: right"
        @click="doCommit()"
        >添加测试项</el-button
      >
    </div>
    <div>
      <el-table :data="testData">
        <el-table-column prop="appId" label="所属应用ID" />
        <el-table-column prop="title" label="测试项标题" />
        <el-table-column prop="tester" label="测试人" />
        <el-table-column prop="version" label="版本" />
        <el-table-column prop="ident" label="标识" />
        <el-table-column :formatter="formatType" prop="type" label="类型" />
        <el-table-column :formatter="formatDate" prop="createDate" label="创建时间" />
        <el-table-column label="操作" width="300">
          <template slot-scope="scope">
            <!--<label>菜单逻辑判断一列</label>-->
            <el-link type="primary" @click="edittestItem(scope.row)">修改测试项</el-link>
            <!--<label>菜单逻辑判断二列</label>-->
            <el-divider direction="vertical"></el-divider>
            <el-link type="primary" @click="scanCase(scope.row)">用例</el-link>
            <el-divider direction="vertical"></el-divider>
            <el-link type="primary" @click="viewItem(scope.row)">测试项表格</el-link>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div>
      <br />
      <el-pagination
        background
        :current-page.sync="pageValues.currentPage"
        :page-size="pageValues.pageSize"
        layout="total, sizes, prev, pager, next"
        :page-sizes="[5, 10, 20, 30, 50]"
        :total="pageValues.total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script>
import { apiAppsProduct } from "@/api/apps";
import { apiTestSearch } from "@/api/test.js";
import moment from "moment";

export default {
  name: "Testitem",
  data() {
    return {
      //条件查询变量定义
      search: {
        productId: "",
        appId: "",
        tester: "",
        type: "",
        ident: "",
        pickTime: "",
      },
      // 范围日期组件的快捷选项配置,也就是上面的pickerOptions
      pickerOptions: {
        shortcuts: [
          {
            text: "最近一周",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getDate() - 3600 * 1000 * 24 * 7);
              picker.$emit("pick", [start, end]); //Vue的4个流程还记得吗
            },
          },
          {
            text: "最近一个月",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
              picker.$emit("pick", [start, end]);
            },
          },
        ],
      },
      //所属分类选项-沿用应用管理
      optsProduct: [],
      //数据表格展示和分页变量定义
      testData: [],
      pageValues: {
        pageSize: 10,
        currentPage: 1,
        total: 0,
      },
    };
  },
  methods: {
    //所属分类选项数据查询,将product表中数据拉出来放入optsProduct
    productList() {
      apiAppsProduct().then((res) => {
        this.optsProduct = res.data;
      });
    },
    //按照条件查询，如果某个控件为空，则不会进行此字段查询
    searchClick() {
      const body = {
        pageSize: this.pageValues.pageSize,
        currentPage: this.pageValues.currentPage,
        productId: this.search.productId,
        appId: this.search.appId,
        tester: this.search.tester,
        type: this.search.type,
        ident: this.search.ident,
        pickTime: this.search.pickTime,
      };
      apiTestSearch(body).then((response) => {
        this.testData = response.data; //放入表格中
        this.pageValues.total = response.total;
        console.log(this.testData);
      });
    },
    formatDate(row, column) {
      const date = row[column.property];
      if (date === undefined) {
        return "";
      }
      // 使用moment格式化时间，由于我的数据库是默认时区，偏移量设置0，各自根据情况进行配置
      return moment(date).utcOffset(0).format("YYYY-MM-DD HH:mm");
    },
    formatType(row, column) {
      const type = row[column.property];
      switch (type) {
        case 1:
          return "功能测试";
        case 2:
          return "接口测试";
        case 3:
          return "性能测试";
        case 4:
          return "文档审查";
        case 5:
          return "代码审查";
        case 6:
          return "静态分析";
        case 7:
          return "余量测试";
        case 8:
          return "人机交互界面测试";
        case 9:
          return "安全测试";
        case 10:
          return "恢复测试";
        case 11:
          return "边界测试";
        case 12:
          return "强度测试";
        case 13:
          return "兼容测试";
        case 14:
          return "安装性测试";
        case 15:
          return "逻辑测试";
        default:
          return "未知状态";
      }
    },
    //增加测试项跳转页面并给个action：ADD的参数
    doCommit() {
      this.$router.push({ name: "commit", params: { action: "ADD" } });
    },
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`);
      this.search.pageSize = val;
      this.searchClick();
    },
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`);
      this.search.currentPage = val;
      this.searchClick();
    },
  },
  created() {
    // 调用methods的方法，即初次加载就请求数据
    this.productList();
    this.searchClick();
  },
};
</script>

<style scoped>
.el-pagination {
  text-align: right;
}
</style>
