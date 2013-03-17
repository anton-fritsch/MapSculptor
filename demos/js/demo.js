(function(){
    DemoBase = function() {
        this.demoContext = $("#demo")[0].getContext('2d');
        this.tileSideLength = 5;
    };

    DemoBase.prototype.draw = function(tilemap){
        for(var col = 0; col < tilemap.length; col++) {
            for(var row = 0; row < tilemap[col].length; row++) {
                this.drawCell(row, col, tilemap[col][row]);
            }
        }
    };

    AutomatonDemo = function() {
        DemoBase.call(this);

        this.states = [
            "rgb(0, 125, 0)", /* Land */
            "rgb(0, 0, 200)", /* Water */
        ];
        $("#title").text("2D Cellular Automaton Demo");
    };

    AutomatonDemo.prototype = new DemoBase();

    AutomatonDemo.prototype.drawCell = function(x, y, state) {
        this.demoContext.fillStyle = this.states[state];
        this.demoContext.fillRect(x * this.tileSideLength,  y * this.tileSideLength, 
                                  this.tileSideLength, this.tileSideLength);
    }; 

    AutomatonDemo.prototype.show = function() {
        var self = this;

        $.ajax({
            url: "/automaton.json",
            cache: false, 
            dataType: "json",
            success: function(data){
                self.draw(data.tilemap);
            }
        });
    };

    PerlinDemo = function() {
        DemoBase.call(this);
        $("#title").text("2D Perlin Noise Demo");

        this.states = [
            "rgb(0, 125, 0)", /* Land */
            "rgb(0, 0, 200)", /* Water */
        ];
    };

    PerlinDemo.prototype = new DemoBase();

    PerlinDemo.prototype.drawCell = function(x, y, state) {
        if (this.showRaw) {
            rgb = "rgb(" + state + ", " + state + ", " + state + ")";
        } 
        else {
            if(state <= 50) { //water
                rgb = "rgb(0, 0, 200)";
            }
            if(state > 50 && state <= 100) { // shallows
                rgb = "rgb(50, 50, 255)";
            }
            else if(state > 100 && state <= 125) { //beach or swamp
                rgb = "rgb(45, 55, 25)";
            }
            else if(state > 125 && state <= 155) { //plains or grass
                rgb = "rgb(0, 125, 0)";
            }
            else if(state > 155 && state < 175) { //something inbetween
                rgb = "rgb(0, 100, 55)";
            }
            else if(state > 175 && state <= 200) { // forest
                rgb = "rgb(0, 75, 55)";
            }
            else if(state > 200 && state <= 225) { //tundra
                rgb = "rgb(175, 175, 225)";
            }
            else if(state > 225) { //mountaintop
                rgb = "rgb(255, 255, 255)";
            }
        }
        this.demoContext.fillStyle = rgb; 
        this.demoContext.fillRect(x * this.tileSideLength,  y * this.tileSideLength, 
                                  this.tileSideLength, this.tileSideLength);
    }; 

    PerlinDemo.prototype.show = function() {
        var self = this;

        $.ajax({
            url: "/perlin.json",
            cache: false,
            dataType: "json",
            success: function(data){
                self.draw(data.tilemap);
            }
        });
    };

    $("#demoSelector").change(function(e){
        var demo;

        switch($(this).val()) {
            case "2dAutomaton":
                demo = new AutomatonDemo();
            break
            case "perlin":
                demo = new PerlinDemo();
            break;
        }
        demo.show();
    });
})();
