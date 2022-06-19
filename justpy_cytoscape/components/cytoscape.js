Vue.component('cytoscapejp', {
    template:
        `<div  v-bind:id="jp_props.id" :class="jp_props.classes"  :style="jp_props.style"  ></div>`,
    data: function () {
        return {
            graph: null
        }
    },
    methods: {
        graph_create() {
            this.graph = this.$props.jp_props.graph;
            //const chart_obj = JSON.parse(this.$props.jp_props.chart);
            //Bokeh.embed.embed_item(chart_obj, 'bokeh' + this.$props.jp_props.id.toString());
            //katex.render(this.$props.jp_props.equation, document.getElementById(this.$props.jp_props.id.toString()), this.$props.jp_props.options);
        }
    },
    mounted() {
        this.graph_create();
    },
    updated() {
        if (this.graph != this.$props.jp_props.graph) {
            // document.getElementById('bokeh' + this.$props.jp_props.id.toString()).innerHTML = "";
            this.graph_create();
        }
    },
    props: {
        jp_props: Object
    }
});

