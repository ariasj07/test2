
import { computed, ref } from 'vue';

export function useAlert(){
    const alert = ref(false)
    const alertIsTrue = ref(true)
    const message = ref('')
    function verify(data){
        if(data.status){
                alert.value = true /* fires the alert */
                alertIsTrue.value = true
                message.value = data.alert
                console.log("si")
                setTimeout(()=>{
                    alert.value = false
                }, 6000)
        }else{
                alert.value = true /* fires the alert */
                alertIsTrue.value = false
                message.value = data.alert
                setTimeout(()=>{
                    alert.value = false
                }, 6000)
        }
    }
    return {
        alert, alertIsTrue, message, verify
    }

}
