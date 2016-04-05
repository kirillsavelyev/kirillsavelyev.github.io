/**
 * Created by ska on 03.04.16.
 */

'use strict';

(function (window, document) {
    var EMPTY_MARK = '';
    var f = [];

    function shuffle(array) {
        var j, x, i;
        for (i = array.length; i; i--) {
            j = Math.floor(Math.random() * i);
            x = array[i - 1];
            array[i - 1] = array[j];
            array[j] = x;
        }
    }

    function create_array(){
        var array = [];
        for(var i = 1; i < 16; i++) { array.push(i); }
        array.push(EMPTY_MARK);
		return array;
    }
	
	function shuffle_array(array){
		shuffle(array);
	}

    function print_field(){
        var puzzle = document.getElementsByClassName('puzzle_field')[0];
        var puzzle_field = document.createElement('div');
        puzzle_field.className = 'puzzle_field';
        for(var i=0; i<16; i=i+4){
            var row = document.createElement('div');
            row.className = 'row_field';

            for(var j=0; j<4; j++){
                var col = document.createElement('div');
                col.textContent = f[i+j];
                col.className = 'col' + col.textContent;
                row.appendChild(col);
            }
            puzzle_field.appendChild(row);
        }
        puzzle.outerHTML = puzzle_field.outerHTML;
    }
	
	function is_game_finished() {
		var win = 0;
		var winner_field = create_array();
		if (winner_field.length === f.length){
			for (var i = 0; i < f.length; i++){
				if (f[i] === winner_field[i]) {
					win++;
				}
			}
		}

		if (win === 16) { alert('Вы выиграли!'); }
	}
	
	function handler(event){
		var KEY_CODE = {
			LEFT: 65,
			UP: 87,
			RIGHT: 68,
			DOWN: 83
			};
		
		var em = f.indexOf(EMPTY_MARK);
        var error = false;

		//function move_alert(){
		//	alert('Нельзя двигать квадрат за пределы поля!')
		//}

		switch(event.keyCode){
			case KEY_CODE.DOWN:
				for (var i=0; i<4; i++){
					if (em === i) {
                        //move_alert();
                        error = true; }
				}
				if (!error) {
                    f[em] = [f[em-4], f[em-4] = f[em]][0]; }
			    break;
			case KEY_CODE.UP:
				for (var j=12;j<16;j++){
					if (em === j) {
                        error = true; }
				}
				if (!error) {
                    f[em] = [f[em+4], f[em+4] = f[em]][0]; }
			    break;
			case KEY_CODE.RIGHT:
				for (var k=0;k<13;k=k+4){
					if (em === k) {
                        error = true; }
				}
				if (!error) {
                    f[em] = [f[em-1], f[em-1] = f[em]][0]; }
                break;
			case KEY_CODE.LEFT:
				for (var n=3;n<16;n=n+4){
					if (em === n) {
                        error = true; }
				}
                if (!error) {
                    f[em] = [f[em+1], f[em+1] = f[em]][0]; }
			    break;
            default:
                error = false;
                //alert('Управление только клавишами WSAD.');
		}
        print_field();
        is_game_finished();
    }
	
	window.addEventListener('keydown', handler, false);

	document.addEventListener('DOMContentLoaded', function() {
        var control = document.getElementById('shuffle');
        control.addEventListener('click', function() {
            run();
        });
    });

    function run(){
        f = create_array();
		shuffle_array(f);
        print_field();
    }

    run();

}) (window, document);
