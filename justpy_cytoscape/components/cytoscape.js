Vue.component('cytoscapejp', {
    template:
    `<div  v-bind:id="jp_props.id" :class="jp_props.classes"  :style="jp_props.style"></div>`,
    data: function () {
        return {
            graph: null
        }
    },
    methods: {
        graph_create() {
            var cy = new cytoscape({
                container: document.getElementById(this.$props.jp_props.id.toString()), // container to render in
                elements: this.$props.jp_props.elements,
                style: this.$props.jp_props.graphstyle,
                layout: this.$props.jp_props.layout
            });
            // Register component
            comp_dict[this.$props.jp_props.id] = cy;
        }
    },
    mounted() {
        this.graph_create();
    },
    updated() {
        if (this.graph != this.$props.jp_props.graph) {
            this.graph_create();
        }
    },
    props: {
        jp_props: Object
    }
});
