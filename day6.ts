const raw = await Deno.readTextFile("./data6.lst");

class Fish {
    ttl: number;

    constructor(ttl: number = 8) {
        this.ttl = ttl;
    }

    tick(): (Fish | null){
        if(this.ttl > 0){
            this.ttl = this.ttl - 1;
            return null;
        }else{
            this.ttl = 6;
            return new Fish();
        }
    }
}

let pool = raw.split(",").map(d => new Fish(parseInt(d)));

const days = 256;
for(let i = 0 ; i <= days ; i++){
    console.log(i, ":", "(",pool.length, ")")//, pool.map(f => f.ttl).join(","))
    const newFishes: Fish[] = []
    pool.forEach(f => {
        const newFish = f.tick();
        if(newFish !== null){
            newFishes.push(newFish);
        }
    })
    pool = pool.concat(newFishes);
    
}