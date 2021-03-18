package skyrama.controller;

import com.google.gson.Gson;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import skyrama.database.Database;
import skyrama.entity.Plane;

import java.util.ArrayList;
import java.util.List;

@RestController
public class Controller {
    Database dat = new Database();
    private ResponseEntity.BodyBuilder ok = ResponseEntity.status(200).contentType(MediaType.APPLICATION_JSON);
    private ResponseEntity.BodyBuilder badRequest = ResponseEntity.status(400).contentType(MediaType.APPLICATION_JSON);
    private ResponseEntity.BodyBuilder notFound = ResponseEntity.status(404).contentType(MediaType.APPLICATION_JSON);

    @PostMapping("/add")
    public ResponseEntity<String> insertPlane(@RequestBody String data){
        Gson gson = new Gson();
        Plane plane = gson.fromJson(data, Plane.class);
        System.out.println(plane.isCargo());
        if (plane.getName() == null || plane.getName().equals(""))
            return badRequest.body(new Gson().toJson("Wrong name"));
        if (plane.getType() == null || plane.getType().equals(""))
            return badRequest.body(new Gson().toJson("Wrong type"));
        if (plane.getCost() <= 0)
            return badRequest.body(new Gson().toJson("Wrong cost of departure"));
        if (plane.getFlight() == null || plane.getFlight().equals(""))
            return badRequest.body(new Gson().toJson("Wrong flight time"));
        if (plane.getDelivery() <= 0)
            return badRequest.body(new Gson().toJson("Wrong delivery"));
        if (plane.getExp() <= 0)
            return badRequest.body(new Gson().toJson("Wrong experience"));
        dat.insertPlane(plane);
        return ok.body(new Gson().toJson("Plane added"));
    }

    @GetMapping("/planes")
    public ResponseEntity<String> getAllPlanes(){
        List<Plane> list = dat.getAllPlanes();
        return ok.body(new Gson().toJson(list));
    }

    @GetMapping(value = "/planes", params = "type")
    public ResponseEntity<String> getPlanesByType(@RequestParam(value = "type") String type){
        if (!(type.equalsIgnoreCase("small")) && !(type.equalsIgnoreCase("medium")) &&
                !(type.equalsIgnoreCase("large")) && !(type.equalsIgnoreCase("searama")) &&
                !(type.equalsIgnoreCase("helicopter")))
            return badRequest.body(new Gson().toJson("Wrong type"));
        List<Plane> list = dat.getPlanesByType(type);
        return ok.body(new Gson().toJson(list));
    }

    @GetMapping(value = "/planes", params = "cargo")
    public ResponseEntity<String> getPlanesByCargo(@RequestParam(value = "cargo") String cargo){
        if (!cargo.equalsIgnoreCase("cargo") && !cargo.equalsIgnoreCase("passenger"))
            return badRequest.body(new Gson().toJson("Wrong cargo type"));
        List<Plane> list = dat.getPlanesByCargo(cargo);
        return ok.body(new Gson().toJson(list));
    }

    @PutMapping(value = "/event", params = "value")
    public ResponseEntity<String> updateEventCurrency(@RequestParam(value = "value") int value){
        if (value < 0)
            return badRequest.body(new Gson().toJson("Wrong value"));
        dat.updateCurrency(value);
        return ok.body(new Gson().toJson("Updated event currency"));
    }

    @GetMapping(value = "/event")
    public ResponseEntity<String> getEventCurrency(){
        return ok.body(new Gson().toJson(dat.getCurrency()));
    }

    @DeleteMapping(value = "/delete", params = "name")
    public ResponseEntity<String> deletePlane(@RequestParam(value = "name") String name){
        if (!dat.exist(name))
            return notFound.body(new Gson().toJson("Cannot find this plane"));
        if(dat.deletePlane(name))
            return ok.body(new Gson().toJson("Plane deleted ;("));
        return badRequest.body(new Gson().toJson(""));
    }


}
