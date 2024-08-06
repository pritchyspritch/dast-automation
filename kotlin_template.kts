import org.apache.commons.httpclient.URI
import org.parosproxy.paros.network.HttpHeader
import org.parosproxy.paros.network.HttpMessage
import org.parosproxy.paros.network.HttpRequestHeader
import org.zaproxy.zap.authentication.AuthenticationHelper
import org.zaproxy.zap.authentication.GenericAuthenticationCredentials
import org.apache.log4j.LogManager

val PARAM_TARGET_URL = "https://pp-services.signin.education.gov.uk/"

val logger = LogManager.getLogger("external-script")

logger.debug("Kotlin auth template 1")

fun authenticate(
        helper: AuthenticationHelper,
        paramsValues: Map<String, String>,
        credentials: GenericAuthenticationCredentials): HttpMessage {

    println("Kotlin auth template 2")

    println("TARGET_URL: ${paramsValues[PARAM_TARGET_URL]}")
    logger.debug("Kotlin auth template")
    logger.debug("TARGET_URL: ${paramsValues[PARAM_TARGET_URL]}")
    val msg = helper.prepareMessage()
    msg.requestHeader = HttpRequestHeader(HttpRequestHeader.GET, URI(paramsValues[PARAM_TARGET_URL], true),
            HttpHeader.HTTP11)
    println("msg: $msg ${msg.requestHeader.headers.size}")
    logger.debug("msg: $msg ${msg.requestHeader.headers.size}")
    msg.requestHeader.headers.forEach { println(it) }
    msg.requestHeader.headers.forEach { logger.debug(it) }
    helper.sendAndReceive(msg)
    return msg
}

fun getRequiredParamsNames(): Array<String> {
    return arrayOf(PARAM_TARGET_URL)
}

fun getOptionalParamsNames(): Array<String> {
    return arrayOf("cookie_file")
}

fun getCredentialsParamsNames(): Array<String> {
    return arrayOf()
}

fun getLoggedInIndicator(): String {
    return "Access DfE services"
}

fun getLoggedOutIndicator(): String {
    return "DfE Sign-in"
}