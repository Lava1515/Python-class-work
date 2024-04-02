
const DivusMaximus = {
    type:"div",
    classname:"",
    id:"",
    onClick:"",
    children:[
        {
            type:"h1",
            classname:"",
            children:{
                type:"text",
                value:"Hello World!",
            }
        }
    ],

}



console.log(DivusMaximus.classname);
DivusMaximus.classname = "yer";
DivusMaximus.children.append()

const CreateDOMElement = (objectAsArray) => {
    let DOMElement = null;
    const BigElement = document.createElement(objectAsArray.type);
    BigElement.classname = objectAsArray.classname;
    BigElement.id = objectAsArray.id;
    objectAsArray.id ? BigElement.id = objectAsArray.id: null;
    
    const Children = objectAsArray.children.map((currentValue, i) => {
        return CreateDOMElement(currentValue)
    })
    return DOMElement;
}