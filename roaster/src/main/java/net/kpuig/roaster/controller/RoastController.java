package net.kpuig.roaster.controller;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;



@RestController
@RequestMapping("/roast")
public class RoastController {
    @PostMapping("/prompt")
    public String postMethodName(@RequestBody String entity) {
        return entity;
    }
    
}
