/* The TileTown 2 box in 3D, shared by the page's looks (with box3d.css):
   each <div class="tt2box"></div> gets the box, dragged (or the arrow keys,
   or Front / Side / Back) to turn; it sways gently until touched (not with
   reduced motion); each side shaded by how much it faces the light. */
(function () {
    var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var HTML = "<div class=\"boxview\" tabindex=\"0\" role=\"img\" aria-label=\"The TileTown 2 box in 3D. Drag it, or use the arrow keys, to turn it. The front: a rainbow stripe, the name TileTown 2 in gold, The City-Building Simulation, the title screen of a little isometric town and a yellow starburst: A city in 3D, 16 maps, 3 levels. The back: the city view and what you need.\"><div class=\"box3d\"><div class=\"bf f\"><i></i></div><div class=\"bf b\"><i></i></div><div class=\"bf l\"><i></i></div><div class=\"bf r\"><i></i></div><div class=\"bf t\"><i></i></div><div class=\"bf u\"><i></i></div></div></div><div class=\"boxbar\"><span>Drag to turn</span><button type=\"button\" data-turn=\"0\">Front</button><button type=\"button\" data-turn=\"90\">Side</button><button type=\"button\" data-turn=\"180\">Back</button></div>";
    function build(holder) {
        holder.innerHTML = HTML;
        var view = holder.querySelector('.boxview');
        /* the box: dragged (or the arrow keys, or Front / Side / Back) to turn;
           it sways gently until touched (not with reduced motion); each side is
           shaded by how much it faces the light */

            var cube = view.querySelector('.box3d');
            var faces = ['f', 'b', 'l', 'r', 't', 'u'].map(function (k) { return view.querySelector('.' + k + ' > i'); });
            var normals = [[0, 0, 1], [0, 0, -1], [-1, 0, 0], [1, 0, 0], [0, -1, 0], [0, 1, 0]];
            var light = [-0.35, -0.35, 0.87];
            var REST = -26, TILT = -8;
            var ry = REST, rx = TILT, vy = 0, goal = null, held = false, touched = false, t0 = performance.now();
            var px = 0, py = 0, lastT = 0, running = false;
            function draw() {
                cube.style.transform = 'rotateX(' + rx + 'deg) rotateY(' + ry + 'deg)';
                var a = rx * Math.PI / 180, b = ry * Math.PI / 180;
                var ca = Math.cos(a), sa = Math.sin(a), cb = Math.cos(b), sb = Math.sin(b);
                normals.forEach(function (n, i) {
                    var x = n[0] * cb + n[2] * sb, z1 = -n[0] * sb + n[2] * cb;
                    var y = n[1] * ca - z1 * sa, z = n[1] * sa + z1 * ca;
                    var lit = Math.max(0, x * light[0] - y * light[1] + z * light[2]);
                    faces[i].style.opacity = (0.6 * (1 - lit)).toFixed(3);
                });
            }
            function tick(now) {
                var busy = held || goal !== null || Math.abs(vy) > 0.02 || (!touched && !still) || Math.abs(TILT - rx) > 0.05;
                if (!held) {
                    if (goal !== null) {
                        var d = goal - ry;
                        ry += d * (still ? 1 : 0.12);
                        if (Math.abs(d) < 0.2) { ry = goal; goal = null; }
                    } else if (Math.abs(vy) > 0.02) {
                        ry += vy; vy *= 0.94;
                    } else if (!touched && !still) {
                        ry = REST + Math.sin((now - t0) / 1700) * 14;
                    }
                    rx += (TILT - rx) * (still ? 1 : 0.05);
                }
                draw();
                if (busy) requestAnimationFrame(tick); else running = false;
            }
            function wake() { if (!running) { running = true; requestAnimationFrame(tick); } }
            function near(target) { return target + Math.round((ry - target) / 360) * 360; }
            view.addEventListener('pointerdown', function (e) {
                held = touched = true; goal = null; vy = 0;
                px = e.clientX; py = e.clientY; lastT = e.timeStamp;
                view.classList.add('drag');
                view.setPointerCapture(e.pointerId);
                wake();
            });
            view.addEventListener('pointermove', function (e) {
                if (!held) return;
                var dx = e.clientX - px, dy = e.clientY - py;
                ry += dx * 0.5;
                rx = Math.max(-35, Math.min(30, rx - dy * 0.35));
                var dt = Math.max(1, e.timeStamp - lastT);
                vy = still ? 0 : dx * 0.5 * Math.min(1, 16 / dt);
                px = e.clientX; py = e.clientY; lastT = e.timeStamp;
                draw();
            });
            function letgo() { held = false; view.classList.remove('drag'); wake(); }
            view.addEventListener('pointerup', letgo);
            view.addEventListener('pointercancel', letgo);
            view.addEventListener('keydown', function (e) {
                if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
                    e.preventDefault(); touched = true; vy = 0;
                    goal = (goal === null ? ry : goal) + (e.key === 'ArrowLeft' ? -30 : 30);
                    wake();
                }
            });
            holder.querySelectorAll('[data-turn]').forEach(function (btn) {
                btn.addEventListener('click', function () {
                    touched = true; vy = 0;
                    goal = near(REST + 26 - (+btn.dataset.turn));
                    wake();
                });
            });
            draw();
            wake();
    }
    document.querySelectorAll('.tt2box').forEach(build);
})();
