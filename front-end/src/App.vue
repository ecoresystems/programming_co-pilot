<template>
    <div id="app">
        <el-button @click="get_copilot" type="primary" style="margin-left: 16px;">open</el-button>

        <el-drawer title="Possible Hits" size="50%" :visible.sync="drawer" :with-header="false">
            <el-row style="padding: 20px">
                Possible Hits
            </el-row>
            <el-row v-for="result in query_result" :gutter="12">
                <el-card shadow="hover">
                    <div>
                        <span v-html="result.Title"></span>
                    </div>
                </el-card>
            </el-row>
        </el-drawer>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                drawer: false,
                content: "",
                comp_output: "",
                language: "",
                query_result: "",
                question_query_time: "",
                answer_query_time: "",
            };
        },
        mounted: function () {
            this.load_sample_data();
        },
        methods: {
            load_sample_data() {
                this.$axios.get("/sample_data.json").then(response => {
                        self.response_data = response.data;
                        this.content = response_data.content;
                        this.comp_output = response_data.comp_output;
                        this.language = response_data.language;
                    }
                )
            },
            get_copilot() {
                this.drawer = true;
                this.$axios
                    .get("http://127.0.0.1:5000/api/get_recommendation", {
                        params: {
                            comp_output: this.comp_output,
                            content: this.content,
                            language: this.language,
                        }
                    })
                    .then(response => {
                        let response_data = response.data;
                        this.query_result = response_data.query_result;
                        this.query_result = JSON.parse(response_data.query_result);
                        this.question_query_time = response_data.question_time;
                        this.answer_query_time = response_data.answer_time;
                        this.$notify({
                            title: "Search successful!",
                            type: "success",
                            message: "Got " + this.query_result.length + " hits in " + (this.answer_query_time + this.question_query_time) + "s",
                            duration: 5000
                        });
                    });
            }
        }
    };
</script>

<style>
    #app {
        font-family: Helvetica, sans-serif;
        /*text-align: left;*/
    }
    .el-drawer{
        height: 100%;
        overflow-y: auto;
    }
    .el-row {
        margin-bottom: 20px;
    &:last-child {
         margin-bottom: 0;
     }
    }

</style>
