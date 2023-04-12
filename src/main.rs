// coding offline rn
// when internet is available {
    // grapher library
// }
fn main() {
    let ob1: Object = Object {
        pos: (1.0, 1.0),
        vel: (0.0, 0.0),
        mass: 1.0,
    };
    let ob2: Object = Object {
        pos: (1.0, -1.0),
        vel: (0.0, 0.0),
        mass: 2.0,
    };
    let ob3: Object = Object {
        pos: (-1.0, -1.0),
        vel: (0.5, 0.2),
        mass: 3.0,
    };
    let mut frame_initial: Frame = Frame {
        obj: vec![ob1, ob2, ob3],
        time: 0.0,
    };
    for _i in 0..10 {
        println!("({}, {})", frame_initial.obj[0].pos.0, frame_initial.obj[0].pos.1);
        println!("({}, {})", frame_initial.obj[1].pos.0, frame_initial.obj[1].pos.1);
        println!("({}, {})", frame_initial.obj[2].pos.0, frame_initial.obj[2].pos.1);
        println!(" ");
        frame_initial = next_frame(frame_initial);
    }
}
static EULER_STEP: f64 = 0.1;
static PI: f64 = 3.1415926535;
// static G: f64 = 0.00000000006674;
static G: f64 = 6.674;

// newtonian gravity sim
// F = m1*m2 / d*d * G
#[derive(Clone)]
struct Frame {
    obj: Vec<Object>,
    time: f64,
}
#[derive(Clone, Copy)]
struct Object {
    pos: (f64, f64),
    vel: (f64, f64),
    mass: f64,
}

fn realsin(x: f64) -> f64 {
    let mut running: f64 = x;
    let mut total: f64 = 0.0;
    for term in 1..8 {
        total += running;
        running *= -x*x / (2*term) as f64 / (2*term+1) as f64;
    }
    total
}
fn realcos(x: f64) -> f64 {
    let mut running: f64 = 1.0;
    let mut total: f64 = 0.0;
    for term in 1..8 {
        total += running;
        running *= -x*x / (2*term) as f64 / (2*term-1) as f64;
    }
    total
}
fn realsqrt(x: f64) -> f64 {
    let (mut t1, mut t2): (f64, f64) = (2.0, 1.0);
    while (t2 - t1).abs() > 0.0001 {
        t1 = t2;
        t2 -= (t2*t2 - x) / (2.0*t2);
    }
    t2
}

fn next_frame(current: Frame) -> Frame {
    let mut new_obj: Vec<Object> = Vec::new();
    for entity1 in &current.obj {
        let mut netforce: (f64, f64) = (0.0, 0.0);
        for entity2 in &current.obj {
            if entity2.pos == entity1.pos { continue }
            let x_dist: f64 = (entity2.pos.0 - entity1.pos.0);
            let y_dist: f64 = (entity2.pos.1 - entity1.pos.1);
            let d2: f64 = x_dist*x_dist + y_dist*y_dist;
            let distance: f64 = realsqrt(d2);
            let force_mag: f64 = G * entity1.mass * entity2.mass / d2;
            netforce.0 += force_mag * x_dist / distance;
            netforce.1 += force_mag * y_dist / distance;
        }
        let vel: (f64, f64) = (entity1.vel.0 + netforce.0 / entity1.mass * EULER_STEP,
            entity1.vel.1 + netforce.1 / entity1.mass * EULER_STEP);
        let pos: (f64, f64) = (entity1.pos.0 + vel.0 * EULER_STEP,
            entity1.pos.1 + vel.1 * EULER_STEP);
        new_obj.push( Object { pos, vel, mass: entity1.mass } );
    }
    Frame { obj: new_obj, time: current.time + EULER_STEP }
}


